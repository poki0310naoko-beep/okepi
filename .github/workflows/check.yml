name: Okepi Monitor
on:
  schedule:
    - cron: '*/5 * * * *' # 5分ごとに実行
  workflow_dispatch: # 手動実行ボタン

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write # これでエラーを防いで保存できるようにします
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4
      - name: Run script
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
        run: python monitor.py
      - name: Commit and Push
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add last_id.txt
          git commit -m "Update last_id" || exit 0
          git push

