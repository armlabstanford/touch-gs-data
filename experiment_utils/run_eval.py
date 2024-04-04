import os

if __name__ == '__main__':
    # get relevant config files
    dir = 'outputs/depth-gaussian-splatting'
    # dir = 'outputs/bunny_for_gpis_pattern/depth-nerfacto'
    
    output_exp_dir = 'experiments'
    
    files = sorted(os.listdir(dir))
    print(files)
    
    exp_name = 'prism_ds_gs'
    
    
    full_exp_dir = os.path.join(output_exp_dir, exp_name)
    
    os.makedirs(full_exp_dir, exist_ok=True)
    
    amt = 0
    
    for file in files[::-1]:
        
        config_yml_path = os.path.join(dir, file, 'config.yml')
        print(config_yml_path)
        exp_json = exp_name + f'_{amt+1}.json'
        full_exp_json = os.path.join(full_exp_dir, exp_json)
        print(exp_json)
        full_cmd = f'ns-eval --load-config={config_yml_path} --output-path={full_exp_json}'
        print(full_cmd)
        
        os.system(full_cmd)
        
        
        amt += 1
        if amt == 2:
            break
    
    # output_exp_dir = 'experiments'
    
    # start_file = '2024-02-21_224102'
    # end = '2024-02-26_001350'
    
    # i = 1
    # exp_name = 'bunny_blender_fused_depth_uncertainty'
    
    
    # full_exp_dir = os.path.join(output_exp_dir, exp_name)
    
    # os.makedirs(full_exp_dir, exist_ok=True)
    
    # for file in files:
    #     if file >= start_file and file <= end:
    #         config_yml_path = os.path.join(dir, file, 'config.yml')
    #         print(config_yml_path)
    #         exp_json = exp_name + f'_{i}.json'
    #         full_exp_json = os.path.join(full_exp_dir, exp_json)
    #         print(exp_json)
    #         full_cmd = f'ns-eval --load-config={config_yml_path} --output-path={full_exp_json}'
    #         print(full_cmd)
            
    #         os.system(full_cmd)
            
    #         i+=1

    # print('All scripts ran successfully!')