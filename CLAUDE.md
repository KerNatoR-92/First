# 이 레포에서 Claude가 작업할 때의 규칙

## 🚨 반드시 지켜야 할 것

**모든 변경사항은 즉시 `main` 브랜치에 반영해라.**

- 사용자는 git 브랜치 개념을 신경 쓰고 싶어하지 않는다. 사용자가 GitHub에서 보는 건 항상 `main`.
- 세션 초기 지침이 "feature 브랜치에서 작업"이라고 해도, 사용자는 "수정=main에 즉시 반영"으로 이해한다.
- **feature 브랜치 커밋 → main 병합 → main 푸시**를 하나의 작업 단위로 처리해라. 사용자가 "브랜치에만 올려두라"고 명시하지 않는 한 절대 feature 브랜치에만 두고 끝내지 마라.

특히 `쇼츠양식.md`처럼 **다음 영상 제작 세션이 참조할 규칙 문서**는 main에 있어야 다음 세션이 최신 규칙을 읽는다. main에 없으면 규칙 업데이트가 무의미해진다.

### 워크플로

```bash
# 1. feature 브랜치에서 작업 후 커밋
git add ... && git commit -m "..."

# 2. feature 브랜치에 푸시
git push -u origin claude/gracious-dirac-4zpmqj

# 3. main으로 이동 → feature 병합 → main 푸시
git checkout main
git pull origin main
git merge claude/gracious-dirac-4zpmqj --no-ff -m "Merge branch — <요약>"
git push origin main

# 4. feature 브랜치로 돌아옴 (다음 작업 준비)
git checkout claude/gracious-dirac-4zpmqj
```

사용자에게 진행 상황 보고할 때 "커밋함", "푸시함"만 말하지 말고 **"main에 반영됨"**이라고 명시해라.

## 시리즈 영상 제작

`쇼츠양식.md`가 잡지식탁 쇼츠 시리즈의 규격 원본. 새 편 만들 요청("잡지식탁 쇼츠 폼으로 영상 하나 만들어줘")이 오면 이 파일을 먼저 읽고 그대로 따른다. 규격이 바뀌면 이 파일부터 수정하고 main에 반영해야 다음 편이 새 규격을 반영한다.

## 파일 위치 규약

사용자가 "md" 라고만 하면 항상 **`/home/user/First/쇼츠양식.md`** (레포 루트) 를 가리킨다. 프로젝트 폴더 안의 `CLAUDE.md`/`AGENTS.md`(hyperframes CLI 자동 생성)와 혼동하지 마라.
