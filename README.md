# NewsFatch — 中国经济新闻抓取

从国内主流媒体抓取经济新闻，并按**可配置日期范围**导出 JSON / Markdown。

## 支持来源

| 标识 | 媒体 |
|------|------|
| `gov_cn` | 中国政府网要闻 |
| `cls` | 财联社电报 |
| `nbd` | 每日经济新闻 |
| `thepaper` | 澎湃新闻（财经相关频道列表） |
| `cs_com_cn` | 中证网 |
| `yicai` | 第一财经 |

## 安装

```bash
cd D:\NewsFatch
python -m pip install -r requirements.txt
```

## 使用示例

抓取**昨天**的全部来源：

```bash
python -m news_fetcher --yesterday
```

指定日期范围与来源：

```bash
python -m news_fetcher --start 2026-09-20 --end 2026-09-22 --sources gov_cn,yicai,thepaper
```

仅元数据、不拉正文（更快）：

```bash
python -m news_fetcher --start 2026-09-22 --end 2026-09-22 --no-body
```

结果默认写入 `output/` 目录：

- `news_YYYY-MM-DD_YYYY-MM-DD.json`
- `news_YYYY-MM-DD_YYYY-MM-DD.md`

## 说明

- 各站点页面结构可能调整；若某来源失败，程序会继续抓取其他来源并在 JSON 中记录错误。
- 部分站点（如财联社、每经网）对网络环境较敏感，超时时可重试或缩小时间范围。
- 澎湃新闻列表当前以首页一批稿件为主，适合日报场景；更广时间范围可结合其他来源。
