from __future__ import annotations

from typing import Any


def build_report_body(nickname: str, deep: bool, supplement: dict[str, Any]) -> dict[str, Any]:
    target = supplement.get("target_audience", "职场 25-35 岁，希望提升个人表达与业务认知的人群")
    goal = supplement.get("goal", "30 天内提升稳定涨粉效率")
    monetization = supplement.get("monetization_mode", "咨询与小课转化")

    common = {
        "report_title": f"{nickname} 账户体检策略简报",
        "summary": f"{nickname} 的增长问题集中在‘主页承接薄弱 + 内容主线分散’，不是流量入口本身。",
        "preview_text": "主页承接薄弱、内容主线分散，建议先做定位收束与7天主线验证。",
        "executive_summary": "先统一主页定位与内容支柱，再做投放节奏。当前最优先动作是重写主页一句话定位，并连续 7 天做同一主线内容。",
        "scores": [
            {"name": "定位清晰度", "score": 63, "reason": "同周内容横跨多个主题，算法标签不稳。"},
            {"name": "主页信任感", "score": 56, "reason": "主页缺少可验证成果和服务对象。"},
            {"name": "内容一致性", "score": 61, "reason": "高表现模板没有系统复用。"},
            {"name": "内容吸附力", "score": 67, "reason": "开头有信息量，但转折不足。"},
            {"name": "转化承接力", "score": 49, "reason": "评论区缺少清晰下一步动作。"},
            {"name": "风险暴露度", "score": 72, "reason": "偶发绝对化表达，有被限流风险。"},
        ],
        "top_issues": [
            {"issue": "账号价值主张不聚焦", "severity": "high", "evidence": "近 10 条内容中主题漂移明显，用户无法形成稳定预期。"},
            {"issue": "主页缺少结果证明", "severity": "high", "evidence": "主页首屏没有案例前后对比，初次访问转粉低。"},
            {"issue": "内容钩子模板复用不足", "severity": "medium", "evidence": "高互动视频开头结构未被复用到后续选题。"},
        ],
        "profile_diagnosis": {
            "current_state": "专业感在，但承诺不够清楚。",
            "problem": "用户 3 秒内看不懂你专门解决谁的什么问题。",
            "suggestion": "主页固定三段：服务对象 + 核心问题 + 可验证结果。",
        },
        "content_diagnosis": {
            "current_state": "内容质量不差但主题分散。",
            "problem": "算法无法稳定打标签，用户难产生追更习惯。",
            "suggestion": "建立三大内容支柱，90% 内容围绕支柱输出。",
        },
        "growth_bottleneck": {
            "key_bottleneck": "曝光到关注转化效率低",
            "why": "主页与内容都没有形成连续的行动引导。",
            "focus_metric": "follow_convert_rate_30d",
        },
        "bottleneck_explanation": "当前瓶颈不是“没流量”，而是“流量来了留不住”。数据上看，平均播放尚可，但关注转化仅 1.3%，说明主页承接与内容连续性是关键缺口。",
        "risk_alerts": [
            "避免使用“保证涨粉”“必火”类绝对化承诺。",
            "商业化信息优先放在评论区置顶，正文少用强营销句。",
        ],
        "action_plan": [
            {"phase": "7d", "action": "主页改版并连发 7 条同主线内容", "expected_outcome": "关注转化率提升到 1.8%-2.2%"},
            {"phase": "30d", "action": "按固定模板迭代 12 条选题并周复盘", "expected_outcome": "内容一致性评分提升到 72+"},
            {"phase": "60d", "action": "放大高互动主题并叠加轻转化动作", "expected_outcome": "形成稳定咨询线索流"},
        ],
        "profile_rewrite_suggestions": {
            "nickname_suggestion": "增长诊断实验室｜{0}".format(nickname),
            "bio_suggestion": "帮 {0} 在 30 天内把内容做成可复用增长系统｜每周更新实操拆解".format(target.split("，")[0]),
            "profile_positioning_statement": "我只解决一个问题：让有专业能力的人，把内容变成稳定增长资产。",
        },
        "content_pillars": [
            {"pillar": "定位纠偏", "why": "先解决“拍什么”这个根问题，避免内容漂移。", "suitable_audience": "有输出意愿但选题反复摇摆的创作者"},
            {"pillar": "脚本结构", "why": "提升前 8 秒留存和完播率，是放大流量的基础。", "suitable_audience": "已有一定流量但完播不稳定的人"},
            {"pillar": "转化承接", "why": "把互动转成关注/咨询，形成可持续商业闭环。", "suitable_audience": "想把内容变成线索来源的创作者"},
        ],
        "seven_day_action_plan": [
            {"day": "day1", "action": "重写昵称、Bio 和主页置顶视频标题。"},
            {"day": "day2", "action": "按“问题-误区-动作”模板重做 1 条主线内容。"},
            {"day": "day3", "action": "复盘近 20 条内容，筛出 3 个高表现开头模板。"},
            {"day": "day4", "action": "发布第二条同主线内容，并统一结尾 CTA。"},
            {"day": "day5", "action": "优化评论区置顶，引导“关注后领取清单”。"},
            {"day": "day6", "action": "发布第三条主线内容，测试不同标题角度。"},
            {"day": "day7", "action": "汇总 7 天数据，确定下周延续的 2 个主题。"},
        ],
        "avoid_now": [
            "先不要横跳到新赛道测试，避免标签再次稀释。",
            "先不要上复杂商业化动作，先把关注转化做稳。",
            "先不要每天换表达风格，保持模板一致性。",
        ],
        "recommended_next_module": "stay_in_account_audit",
        "routing": {
            "recommended_module": "account-audit",
            "reason": f"当前首要目标为 {goal}，先修复账号底层结构更划算。",
            "next_step": "7 天行动计划执行后，再进入下一模块。",
        },
    }

    if not deep:
        return common

    common["deep_insight"] = {
        "audience_fit": f"当前内容更匹配 {target}，建议减少泛人群表达。",
        "monetization_path": f"推荐“公开内容种草 + 私域咨询承接”，更符合{monetization}目标。",
        "content_engine": "建立“问题库 -> 脚本模板 -> 评分复盘”三层机制。",
    }
    common["benchmark_hint"] = {
        "peer_gap": "同量级优质账号相比，你的主页证据密度约低 35%。",
        "opportunity": "你在案例拆解类内容互动效率已接近头部中位值。",
        "priority": "先打稳主页+主线，再扩大选题外延。",
    }
    common["recommended_next_module"] = "niche_map"
    return common
