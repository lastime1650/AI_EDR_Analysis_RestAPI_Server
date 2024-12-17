EDR 시스템 자체에서 제공하는 "외부 분석 기능"입니다. 

이 말은 즉, 외부 분석 기능-> "VirusTotal, Yara,,,"의 분석 함수를 제공한다는 말이며,

사용자가 직접 이 분석 서버에 "자신만의 분석 스크립트"에서 "외부 분석 기능"을 사용할 때는, 다음과 같은 PROVIDER_ANALYSIS_SCRIPT에 있는
Provider_service.py를 사용하면 됩니다. 

scripts 폴더 이하에 있는 것들은 이미 Provider_service.py에서 알아서 호출하도록 설계되었으므로 만질 필요가 전혀 없습니다.
