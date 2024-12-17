'''
    기본 제공형 스크립트 패키지
'''
import queue


import _Analysis_Server_.PROVIDER_ANALYSIS_SCRIPT.scripts.YARA.YARA as YARA


class Provider_Analysis_service:
    def __init__(self):
        self.YARA = YARA.Yara_Analyzer()

    def Yara_Analysis(self, analysis_target_bin: bytes)->queue.Queue:
        #  외부 스크립트가 해당 Yara 분석을 요구하고 있음
        return self.YARA.Start_Analysis(analysis_target_bin) # 비동기 분석 요청이므로 큐를 반환