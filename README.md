# Text-Story-Engine (TSE)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-886FBF?logo=googlegemini&logoColor=fff)](#) [![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#) [![JSON](https://img.shields.io/badge/JSON-000?logo=json&logoColor=fff)](#)

---

### 1. 프로젝트 개요

- **프로젝트명**: TextStoryEngine (TSE)
- **목적**: 텍스트 기반 스토리 게임을 위한 파이썬 엔진. 플레이어 선택지에 따라 스토리가 진행되며, Gemini API를 통해 동적 스토리 생성 지원.
- **주요 기능**:
    - 텍스트 출력 및 사용자 입력 처리
    - JSON 기반 스토리 스크립트 관리
    - 선택지 기반 스토리 분기
    - Gemini API를 활용한 실시간 스토리/대사 생성
    - 게임 상태 저장/불러오기
- **대상 사용자**: 게임 개발자, 스토리 창작자
- **언어 및 도구**: Python 3.x, google.generativeai, JSON

### 2. 엔진 요구사항

- **모듈성**: 스토리 관리, 입력 처리, AI 통합을 별도로 구성.
- **확장성**: 다른 AI API나 사용자 정의 스크립트를 추가 가능.
- **사용자 경험**:
    - CLI 인터페이스 (터미널에서 동작).
    - 텍스트에 색상 및 서식 추가 (colorama 사용).
- **AI 통합**: google.generativeai를 통해 Gemini API 호출, 스토리 콘텐츠 생성.
- **데이터 구조**: JSON 파일로 기본 스토리와 분기 관리.

### 3. 시스템 구조

- **story_manager.py**: 스토리 데이터 로드 및 분기 처리.
- **io_handle.py**: 사용자 입력 수집 및 검증.
- **gen_support.py**: Gemini API 호출 및 응답 처리.
- **main.py**: 엔진의 메인 루프와 통합.

### 4. 기술 스택

- Python 3.10 이상
- 외부 라이브러리:
    - google-generative-ai (Gemini API용)
    - colorama (터미널 텍스트 스타일링)
- 데이터 포맷: JSON
