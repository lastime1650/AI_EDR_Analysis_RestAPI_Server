import enum
import sys
import types
import importlib.util
from typing import Optional
import queue

# 스크립ㅌ트 타입 ENUM값
class Script_Packages_type_enum(enum.Enum):
    file = 0
    network = 1

class Script_Packages:
    def __init__(self):
        self.scripts = {}

    def Add_Script(self, script_name: str, script_type: Script_Packages_type_enum, python_code: str) -> bool :

        if script_name in self.scripts:
            return False

        # 새로운 모듈을 생성합니다.
        module = types.ModuleType(script_name)

        # sys.modules에 모듈을 추가하여 import 가능
        sys.modules[script_name] = module

        # python_code가 실행될 떄 모든 모듈의 접근이 가능하도록 함.  ( 위험하긴 해 )
        for name, existing_module in sys.modules.items():
            if hasattr(existing_module, "__dict__"):
                module.__dict__[name] = existing_module

        # 문자열 스크립트를 모듈에서 실행합니다.
        exec(python_code, module.__dict__)

        # 최종 저장
        self.scripts[script_name] = {
            "module": module,
            "type": script_type.name,# 문자열로 저장
        }

        return True

    def remove_script(self, script_name:str)->bool:
        if script_name in self.scripts:
            del self.scripts[script_name]
            return True
        else:
            return False

#-------------------------------------------------------------------------------------------------------------------------

    # type은 이미 정해진것.
    # script_names는 에이전트가 현재 사용가능한 이름이여하며, script_packages에 등록하고 있어야하는 정보.
    def Start_Analysis(self, script_type:Script_Packages_type_enum, blacklist_script_names:list, DATA:bytes) -> Optional[dict] :

        queue_list = []

        output = {
            "Analysis_Results": []
        }

        for script_name in self.scripts:

            # 블랙리스트 스크립립트는 제외하고, 타입이 다른 스크립트는 제외한다.
            if script_name in blacklist_script_names or self.scripts[script_name]["type"] != script_type.name: continue

            queue_instance = queue.Queue()

            queue_list.append( self.scripts[script_name]["module"].Start_Analysis(queue_instance, DATA) )

        # 모두 완료할 때까지 대기
        for q in queue_list:
            output["Analysis_Results"].append( q.get() )

        return output

    # 현 등록한 스크립트 조회
    def Get_script(self, script_type:Script_Packages_type_enum = None, with_script_name:str = None)->Optional[dict]:
        if not script_type and not with_script_name:
            return None
        if with_script_name and not script_type:
            if with_script_name in self.scripts:
                output = {
                    "module": self.scripts[with_script_name]["module"].__name__,
                    "type": self.scripts[with_script_name]["type"]
                }
                return output
            else:
                return None
        elif script_type and not with_script_name:
            output = {}
            for script_name_v in self.scripts:
                if self.scripts[script_name_v]["type"] == script_type.name:
                    output = {
                        "module": self.scripts[script_name_v]["module"].__name__,
                        "type": self.scripts[script_name_v]["type"]
                    }
            return output
        else:
            # 모두 존재하는 경우,
            for script_name_v in self.scripts:
                if self.scripts[script_name_v]["type"] == script_type.name and self.scripts[script_name_v]["module"].__name__ == with_script_name:
                    return {
                        "module": self.scripts[script_name_v]["module"].__name__,
                        "type": self.scripts[script_name_v]["type"]
                    }
            return None


# python_code 수정 (Script_Packages를 import하여 사용)
python_code = """
import queue
import threading

def custom(queue_instance:queue.Queue, DATA:bytes):
  print(f"Analysis -> {DATA}")
  
  queue_instance.put({"custom_res":DATA}) # 완료
  return 

# 기본 구조
def Start_Analysis(queue_instance:queue.Queue, DATA:bytes):
    thread = threading.Thread(target=custom, args=(queue_instance, DATA))
    thread.start()
    
    return queue_instance

"""

# Script_Packages 인스턴스 생성
#script_packages = Script_Packages()

# 모듈 생성
# = script_packages
#my_module.Append_Script("my_module", "file", python_code, True)
#print( my_module.Start_Analysis("file", ["my_module"], b"Hello") )

