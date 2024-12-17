
import hashlib
import os

#------- Yara ---------------------------------------------------------------------------------------------------------
import yara
import Analysis_System.Utility.File_Explorer.File_Manager as File_Manager

#--
import threading, queue

# Yara Rule을 이용하여 파일을 분석한다.
class Yara_Analyzer:
    def __init__(self,Rules_folder_ROOT_path:str=None  ):
        if Rules_folder_ROOT_path == None:
            # 이 경우 절대적으로 지정.
            Rules_folder_ROOT_path = r"C:\Users\Administrator\Desktop\My_Python_Prj\NewGen_EDR\pythonProject\_Analysis_Server_\PROVIDER_ANALYSIS_SCRIPT\scripts\YARA\yara_rules"

        self.Rules_folder_path = []
        if(Rules_folder_ROOT_path):
            self.Rules_folder_path = File_Manager.File_Manager(Rules_folder_ROOT_path).Searching_Files("yar")
            print(self.Rules_folder_path)
        else:
            raise Exception("Yara 분석 경로를 지정해주세요.")






    # 분석이 자동화로 시작할수 있는 기본 형식임 ( 이 메서드 이름과 인자는 절대 변경하면 안됨
    def Start_Analysis(self, Analysis_target:any):
        print("yara")
        queue_inst = queue.Queue() # 이거 없어서 무조건 None
        thread = threading.Thread(target=self.Running, args=(Analysis_target, queue_inst))
        thread.start()
        return queue_inst


    def Running(self, Analysis_target:any, queue_inst:queue.Queue):

        result = {
            "target_sha256": "",
            "yara_detected_by_rule": [],
            "status": "failed"
        }

        binary = b''
        # 분석 대상 추출
        if isinstance(Analysis_target, str):
            File_Path = Analysis_target
            binary = open(File_Path, 'rb').read()
            result["target_sha256"] = hashlib.sha256(binary).hexdigest()
        elif isinstance(Analysis_target, bytes):
            binary = Analysis_target
            result["target_sha256"] = hashlib.sha256(binary).hexdigest()
        else:
            queue_inst.put(result) # 결과 리턴
            return

        # rule 탐지 실시
        rule_detected_by_yara = []
        for yara_file in self.Rules_folder_path:

            # Yara 컴파일
            try:
                yara_rule_instance = yara.compile(filepath=yara_file)
            except:
                continue

            # 매칭 실시
            matches = yara_rule_instance.match(data=binary)

            # 결과 추출
            if(len(matches)>0):
                # rule 일치하였을 때
                for matched_rule_name in matches:
                    rule_detected_by_yara.append({
                        "rule_name": str(matched_rule_name),
                        "description": matched_rule_name.meta["description"] if "description" in matched_rule_name.meta else "이 규칙에는 따로 해석이 없습니다.",
                    })

        # 결과 정리
        result["status"] = "success"
        result["yara_detected_by_rule"] = rule_detected_by_yara
        queue_inst.put(result)
        return


# (1) 야라 분석 ROOT 폴더 지정
#my_yara_inst = Yara_Analyzer(r".\yara_rules")

# (2) 분석 대상 파일 지정 또는 바이너리 가능!
#target: any = None
#target = r"C:\Users\Administrator\Desktop\KDU\kdu.exe"
#target = open(r"C:\Users\Administrator\Desktop\KDU\kdu.exe", 'rb').read()

# (3) 비동기 분석 요청
#queue_instance = my_yara_inst.Start_Analysis( target)

# (4) 분석 결과 얻어오기
#yara_result = queue_instance.get() # 하나의 데이터만 기다리면 됩니다. !@
#print(yara_result)


