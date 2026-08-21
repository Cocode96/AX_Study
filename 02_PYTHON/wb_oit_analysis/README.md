# WB-OIT Effect Preset Analysis

마비노기 모바일 모작의 `EffectPresets` JSON을 읽어 WB-OIT 설정 경향을 분석한다.

## 실행

`AX_Study/02_PYTHON`에서 실행한다.

```powershell
uv run python wb_oit_analysis/analyze_wb_oit.py
```

다른 데이터 경로를 분석하려면 다음처럼 지정한다.

```powershell
uv run python wb_oit_analysis/analyze_wb_oit.py --preset-dir "C:\path\to\EffectPresets"
```

결과는 기본적으로 `wb_oit_analysis/output`에 생성된다.

- `wb_oit_presets.csv`: JSON 한 파일당 한 행인 정제 데이터
- `wb_oit_summary.csv`: 효과 분류와 모드 조합별 요약 통계
- `wb_oit_dashboard.png`: 모드, 분류, 밝기와 파라미터 관계
- `wb_oit_weight_curves.png`: 자주 사용한 설정의 alpha별 weight 곡선

## 코드에서 확인한 모드

```text
AlphaMode 0: Pow    = pow(alpha, pAlpha) * kAlpha
AlphaMode 1: LinExp = 1 - exp(-alpha * kAlpha)
DepthMode 0: None   = 1
DepthMode 1: Exp    = exp(-z_ndc * kDepth)
최종 weight          = alpha weight * depth weight
```

## 분류 기준

효과 종류는 파일명과 `GameObjectName`, 모델명, 텍스처명에 포함된 영문 키워드로
분류한다. 하나의 preset이 여러 키워드에 해당하면 코드에 정의된 우선순위를 따른다.
따라서 이 열은 정답 라벨이 아니라 데이터 탐색을 위한 휴리스틱이다.

색상은 JSON 안에서 이름에 `Color`가 포함된 RGB 배열을 수집해 평균을 낸다.
C++ 코드에서 확인한 Point/Quad 흰색, Bloom 흰색, Mesh gradient 빨강/검정 기본값은
사용자 지정 색상 후보에서 제외한다. 남은 RGB가 없으면 텍스처에 색이 들어 있거나
엔진 기본값을 사용한 경우이므로 `engine_default_or_texture`로 남긴다. 텍스처 이미지를
실제로 샘플링하지 않으므로 이 경우의 밝기와 색상은 추측하지 않는다.

`GradientBrightColors`, `GradientDarkColors`, `BloomColorPerMesh`, 파티클의
시작/종료 색상처럼 JSON에 저장된 값은 모두 후보에 포함된다. 검정과 흰색 기본값도
실제 설정값과 구분할 수 없으므로 `color_source_count`를 함께 확인하는 것이 좋다.
