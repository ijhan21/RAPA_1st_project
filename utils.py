# UI 클래스
class UI:
    def __init__(self):
        # tkinter or Web 구현
        pass
    
# 백엔드 클래스
class Motion_Detect: #카메라로부터 데이터 받아서 동작과 연결
    def __init__(self):
        # GetData연결        
        # Action 클래스 초기화
        pass
    def motion_to_action(self):
        # if A조건: A행동
        # elif B조건 : B행동
        pass
    # 어떤 알고리즘으로 연계되는 행동을 인식하여 반영할 것인지 고민

class GetData:
    def __init__(self) -> None:
        # 카메라 초기화
        # 데이터 수집
        pass
    # 안정적인 손가락 정보 인식 전달 목표
    # 손가락 이외의 기능 추가 여부 검토    

# Action 클래스
class Action:
    def __init__(self):
        # ppt 초기화
        # ppt 관련 행동 정의
        pass
    
    def action_left(self): # 이전 화면으로 전환
        raise NotImplementedError
    def action_move_next(self): # 다음 화면으로 전환
        raise NotImplementedError

    # 다양한 프로그램 연결이 가능하도록 구성
    
class Action_ppt(Action):
    def __init__(self):
        super().__init__()
        pass