import os
import re
import csv
import json
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from app.config import Config

TOKEN_REGEX=re.compile(r"<Tkn\d{3}[A-Z]{5}Tkn>")

def scan_single_file(file_path, root_path):
    file_findings={}
    try:
        with open(file_path,'r',errors='ignore',encoding='utf-8') as f:
            content=f.read() 
            matches=TOKEN_REGEX.findall(content)
            for token in matches:
                file_findings[token]=file_findings.get(token,0)+1
    except Exception:
        pass  
    if not file_findings:
        return []

    relative_path=os.path.relpath(file_path,root_path)
    results=[]
    for token,occurrences in file_findings.items():
        results.append({
            "Path":relative_path,
            "Token":token,
            "Occurrences":occurrences
        })
    return results

def analyze_firmware(directory_path, csv_output_path):
    all_files=[]
    for root, _,filenames in os.walk(directory_path):
        for filename in filenames:
            all_files.append(os.path.join(root,filename))

    aggregated_results=[]
    with ThreadPoolExecutor(max_workers=Config.CONCURRENCY) as executor:
        futures=[executor.submit(scan_single_file,f,directory_path) for f in all_files]
        for future in futures:
            aggregated_results.extend(future.result())
            
    aggregated_results.sort(key=lambda x:(x["Path"],x["Occurrences"],x["Token"]))

    output_directory=os.path.dirname(csv_output_path)
    if output_directory:
        os.makedirs(output_directory,exist_ok=True)

    with open(csv_output_path,'w',newline='',encoding='utf-8') as csvfile:
        fieldnames=['Path','Token','Occurrences']
        writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in aggregated_results:
            writer.writerow(row)
            
    global_stats=defaultdict(int)
    for item in aggregated_results:
        global_stats[item["Token"]]+=item["Occurrences"]

    final_json_stats=dict(global_stats)
    print(json.dumps(final_json_stats))
    return final_json_stats
