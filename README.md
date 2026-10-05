# persuasion-check

데이터 보고서, 한 장 제안서, 대시보드를 **결정권자에게 내기 전에** 설득력을 점검하는 Claude Code / Codex 스킬.

글을 그럴듯하게 다듬지 않는다. 상대가 판단하기 어렵게 만드는 곳, 근거보다 세게 말한 곳, 보는 사람을 잘못 이끄는 곳을 찾아 "지금 → 이렇게"로 보여 주고, 고칠지는 사람이 정한다.

## 무엇을 보나

| 축 | 질문 | 보는 것 |
|---|---|---|
| 공감 | 결정권자가 자기 이야기로 읽는가 | 첫 줄이 그의 결정인가, 제약이 반영됐나, 결말(요청)이 있나 |
| 형태 | 이 조직에 맞는 그릇인가 | 거버넌스 × 활용 수준 여섯 문항 → 탐색형, 요약형, 해석형 |
| 논리 | 근거에서 결론까지 가도 되는가 | 사실과 해석 구분, 근거 숫자 대조, 비교 기준, 다른 설명, 차트의 인지 위험 여덟 가지 |

마지막에 결정권자 역할로 반론 셋을 던져 리허설한다.

`scripts/number_check.py`(표준 라이브러리만 사용)가 결과물의 숫자 중 근거 폴더 어디에도 없는 것을 찾는다. 반올림, '약', 만 원과 백만 원, 억 환산까지 맞춰 본다.

## 설치

폴더째 넣으면 된다.

```bash
git clone https://github.com/thinknod/persuasion-check.git
# Claude Code
mkdir -p .claude/skills && cp -R persuasion-check/skills/persuasion-check .claude/skills/
# Codex
mkdir -p .agents/skills && cp -R persuasion-check/skills/persuasion-check .agents/skills/
```

## 쓰는 법

```
산출물/5_한장제안.md 를 대표에게 내기 전에 설득력 점검해 줘. 근거는 산출물/ 폴더에 있어.
```

결과는 결과물 옆 `<이름>_설득점검.md`. 원본은 고치지 않는다. 결정권자, 기한, 선택지를 모르면 먼저 묻고 멈춘다.

숫자 대조만 따로:

```bash
python3 skills/persuasion-check/scripts/number_check.py 보고서.md 근거폴더/
```

## 시험해 본 결과

`evals/files/weak-report/`에 약점 11개를 일부러 숨긴 가상 보고서가 있다(가상 쇼핑몰 데이터, 실제 회사나 사람 없음). 이 스킬로 11개를 모두 찾았고, 표 합계가 노트와 다른 것 하나를 더 찾았다. 잘 만든 대시보드에서는 실제 문제만 짚었다.

## 한계

- 설득력을 높여도 답이 옳아지지는 않는다. 분석이 틀렸으면 분석으로 돌아가야 한다
- number_check는 "근거에서 찾지 못했다"만 알려 준다. 틀렸다는 뜻이 아니라 출처를 물어야 한다는 뜻이다
- 코드가 그리는 대시보드의 화면 숫자는 스크립트가 읽지 못한다. 캡처와 생성 코드를 직접 대조한다
- 형태 판정의 조직 점수는 추정이면 추정이라고 쓰고 확인받는다

## 근거

장서우(2026), 「데이터 기반 설득을 위한 커뮤니케이션 디자인 모델 프로세스 및 수용성 검증 연구」, 홍익대학교 국제디자인전문대학원 박사학위논문. 공감(인물, 배경, 플롯), 형태(데이터 형태 선정 도구 [표 11], 조직 맥락에 따른 형태 [표 12]), 논리(감각, 이해, 기억 단계와 인지 설계 리스크 [표 10])를 점검표로 옮겼다. 표는 요약해 옮겼고 원문은 논문을 본다.

함께 참고: Barbara Minto, 피라미드 원칙 / Kaiser Fung, Junk Charts 트라이펙타(질문, 데이터, 화면).

## English

`persuasion-check` is a skill for Claude Code and Codex that reviews a data report, one-page proposal or dashboard before it goes to a decision-maker. It checks three axes adapted from rhetoric for data communication (empathy: whose decision and constraints; form: exploratory / summary / interpretive format matched to the audience's data governance and literacy; logic: fact vs. interpretation, numbers traceable to the evidence folder, comparison baselines, rival explanations and eight cognitive risks in charts), picks the top three fixes as "now → instead", and rehearses three objections in the decision-maker's role. It never rewrites the original. The bundled `number_check.py` (stdlib only) lists numbers in the report that cannot be found in the evidence folder. Instructions are in Korean. Based on Chang (2026), doctoral dissertation, Hongik University.

## 라이선스

MIT. 논문 내용은 출처를 밝혀 요약해 인용했다.
