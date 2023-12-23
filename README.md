# Installation
1. Git clone: 
    ```
    git clone https://github.com/hieuleminh03/SyncLocalWithS3Bucket
    ```
2. Install requirements.txt
    ```bash
    pip install requirements.txt
    ```
3. Go to AWS, create a IAM user with **full access** to AWS S3
4. Run the script
    ``` bash
    python service.py 
        -f path_to_local_folder 
        -t back_up_time_in_seconds 
        -u access_key 
        -p secret_access_key 
        -b bucket_name
    ```
