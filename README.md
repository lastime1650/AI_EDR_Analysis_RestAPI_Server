# AI_EDR_Analysis_RestAPI_Server
This code is a server development that belongs to the development of the "LLM-based EDR system". Among multiple servers, implement an "analysis server".

</br>

# AI EDR의 서버 중에 해당하는 "분석 서버" 개발 코드
본 코드는 AI EDR 시스템 개발의 속하는 "분석 서버"입니다.

Python으로 구현되며, RestAPI는 "FAST API" 로 개발되었습니다.

이 분석 서버는 "사용자 정의 형 분석스크립트"형태로 사용자가 작성한 스크립트를 실행가능한 형태(module)로 변환하여 관리하는 서버입니다.

</br>

# 어떻게 사용하는가? 

먼저, 아래 3가지 python code가 존재합니다.

1. [Analysis_Server.py](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/main/codes/Analysis_Server.py) (RestAPI동작코드)
2. [codes/AGENT_INSTANCE/Agent_based_instance.py](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/main/codes/AGENT_INSTANCE/Agent_based_instance.py) (에이전트기반 관리 인스턴스)
3. [codes/SCRIPT_PACKAGES/Script_Packages.py](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/main/codes/SCRIPT_PACKAGES/Script_Packages.py) (스크립트 관리 인스턴스)

실제 사용하기 위해서는 소스코드를 다운로드하고, import부분을 적절히 환경에 맞춰 수정하셔야합니다.
그런 다음 이미 작성된 실행코드가 포함된 Analysis_Server.py를 실행하면 됩니다.

# 이게 무슨 코드인가? (상세한 설명)

## 제목
![initial](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/main/images/%EC%8A%AC%EB%9D%BC%EC%9D%B4%EB%93%9C1.PNG)
이는 "사용자 정의"라고 하여, 사용자가 직접 작성한 파이썬기반의 분석 스크립트를 실행가능한 Module형태로 변환하여 런타임내에서 분석을 진행하는 서버입니다. 

## 왜 이 서버를 개발하게 되었는가? 
![initial](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/main/images/%EC%8A%AC%EB%9D%BC%EC%9D%B4%EB%93%9C2.PNG)
분석 서버를 유일하게 많이 호출하는 "코어 서버"는 "이벤트 수집", "LLM 평가" 를 진행합니다. 하지만, 이벤트를 수집한 것들을 "바로 LLM에게 평가요청"하는 것은 환각현상에 의해 객관적 정보가 떨어져 응답을 생성할 위험이 있습니다. 그리하여 이 분석 서버를 따로 만들어 "분석 정보(객관적 정보)"를 얻고, 이를 수집된 데이터와 포함하여 LLM에게 평가요청해야 정확도가 올라갈 수 있습니다.

## "분석 서버" 도입시 어떤 흐름인가?
![initial](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/main/images/%EC%8A%AC%EB%9D%BC%EC%9D%B4%EB%93%9C3.PNG)
분석 서버를 도입하면, 이벤트 하나당 분석 요청을 할 수 있으므로, 일단 분석 서버에서의 분석은 "비동기"적으로 수행되어야합니다. 또한, 이벤트 수집 시 유형(프로세스, 파일, 네트워크,,,)에 따라 지원하는 스크립트여야하며, 결과는 한번에 반환해야합니다. 분석 결과는 사용자가 추가한 스크립트 반환에 따라 의존됩니다. (단, Dictionary여야만함 )

## "분석 서버" 구조
![initial](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/main/images/%EC%8A%AC%EB%9D%BC%EC%9D%B4%EB%93%9C4.PNG)
분석 서버는 위 사진과 같이 구성됩니다. 

1. 에이전트 관리 인스턴스 - [codes/AGENT_INSTANCE/Agent_based_instance.py](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/main/codes/AGENT_INSTANCE/Agent_based_instance.py)
2. 스크립트 관리 인스턴스 - [codes/SCRIPT_PACKAGES/Script_Packages.py](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/main/codes/SCRIPT_PACKAGES/Script_Packages.py)
3. 분석 가능한 에이전트 목록 - [codes/AGENT_INSTANCE/Agent_based_instance.py, self.Agent_infos](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/1c3079dbb93288d71fab8edff7980b04c34964b7/codes/AGENT_INSTANCE/Agent_based_instance.py#L8)
4. 등록된 스크립트 목록 - [codes/SCRIPT_PACKAGES/Script_Packages.py, self.scripts](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/1c3079dbb93288d71fab8edff7980b04c34964b7/codes/SCRIPT_PACKAGES/Script_Packages.py#L15)

## 파이썬 기반의 분석 스크립트 구조
![initial](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/main/images/%EC%8A%AC%EB%9D%BC%EC%9D%B4%EB%93%9C5.PNG)
```python
import queue # 필수
import threading # 필수

def custom(queue_instance:queue.Queue, DATA:bytes):
  print(f"Analysis -> {DATA}")
  
  queue_instance.put({"custom_res":DATA}) # 완료, 필수 ( 반환 꼭 해야지 )
  return 

# 기본 구조
def Start_Analysis(queue_instance:queue.Queue, DATA:bytes): # 필수 
    thread = threading.Thread(target=custom, args=(queue_instance, DATA)) # 필수
    thread.start() # 필수 
    
    return queue_instance # 필수
```

## 시나리오
![initial](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/main/images/%EC%8A%AC%EB%9D%BC%EC%9D%B4%EB%93%9C6.PNG)
* [text로 받은 Python code는 무조건 module로 변환해야합니다.](https://github.com/lastime1650/AI_EDR_Analysis_RestAPI_Server/blob/1c3079dbb93288d71fab8edff7980b04c34964b7/codes/SCRIPT_PACKAGES/Script_Packages.py#L23)
