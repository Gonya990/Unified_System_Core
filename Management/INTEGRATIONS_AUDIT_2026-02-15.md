# Integrations Audit

Date: 2026-02-15
Scope: Repository evidence only (local code/config). External account status not verified.

Legend (Status):
- In code: used or referenced by code paths.
- Infra/UI: local network or admin console; not directly called by code.
- Portal/Docs: management or documentation pages.
- Not found: no repo evidence found.

## Links Audit Table

| Link / Service | Status | Repo Evidence (paths) | Recommended Action |
| --- | --- | --- | --- |
| https://aistudio.google.com/ | Portal/Docs | `LLM_Council/council/providers/gemini_provider.py`, `Projects/AI_Core/src/inference_client.py` | Keep for Gemini key management. |
| https://console.cloud.google.com/iam-admin/serviceaccounts/details/117952818893914303624;edit=true/permissions?project=my-home-435112 | Portal/Docs | `Projects/AI_Core/src/google_auth.py`, `Scripts/monitoring/metrics_collector.py` | Keep for IAM/service accounts. |
| https://chatgpt.com/ | Portal/Docs | OpenAI used in code, but ChatGPT UI not used directly | Optional; not needed for API. |
| https://platform.openai.com/docs/overview | Portal/Docs | `LLM_Council/council/providers/openai_provider.py`, `Projects/Content_Factory/src/researcher/daily_researcher.py` | Keep (docs). |
| https://console.cloud.google.com/cloud-resource-manager?project=my-home-435112 | Portal/Docs | GCP integrations in code (see above) | Keep (admin). |
| https://build.nvidia.com/explore/run-on-rtx | Portal/Docs | `LLM_Council/council/providers/nvidia_nim.py`, `nixos-cluster/modules/nvidia.nix` | Optional; use if enabling RTX inference. |
| https://gemini.google.com/app/5644134c3e6e9a43 | Portal/Docs | Gemini API used; Gemini UI not referenced | Optional (manual). |
| https://grok.com/ | Not found | No repo references | If not needed, can ignore/remove account. |
| https://serpapi.com/dashboard | In code | `Projects/AI_Core/src/web_search.py`, `Scripts/Integrations/serpapi_search.py` | Keep if using web search. |
| https://colab.research.google.com/ | Not found | No repo references | Optional/manual. |
| https://dialogs.yandex.ru/developer/skills/95880a09-6dec-4895-9522-938c89bde302/draft/settings/main | In code (Yandex Alice) | `Projects/AI_Core/src/alice_skill.py`, `Scripts/automation/start_alice_tunnel.sh` | Keep if Alice skill is active. |
| https://linear.app/igoryan/team/IGO/active | In code | `Projects/AI_Core/src/linear_client.py` | Keep if Linear automation used. |
| https://platform.openai.com/docs/libraries?language=csharp#install-an-official-sdk | Portal/Docs | OpenAI used in code | Optional docs. |
| https://aistudio.google.com/prompts/new_chat?utm_source=the_keyword&utm_medium=blog&utm_campaign=g3-q4-25 | Portal/Docs | Gemini API used | Optional. |
| https://developer.nvidia.com/ai-apps-for-rtx-pcs/inference-backends | Portal/Docs | NVIDIA NIM/GPU config in repo | Optional. |
| http://192.168.1.216:8123/home/overview | Infra/UI (Home Assistant) | `Projects/AI_Core/src/ha_controller.py`, `Projects/AI_Core/src/ha_client.py` | Keep if HA automation needed. |
| http://smart.tail5e8a72.ts.net:8123/hacs/dashboard | Infra/UI (Home Assistant) | Same as above | Keep if HA integration used. |
| https://aistudio.google.com/api-keys | Portal/Docs | Gemini API used | Keep for key management. |
| https://console.cloud.google.com/billing/011CFE-33CC55-CEFB8F | Portal/Docs | GCP APIs used | Keep for billing control. |
| https://console.cloud.google.com/apis/dashboard?project=gen-lang-client-0982257437 | Portal/Docs | GCP APIs used | Keep for API enablement. |
| https://app.electricitymaps.com/datasets?zone=IL | Not found | No repo references | Optional/manual. |
| https://192.168.190.126/kvm/ | Infra/UI (Proxmox) | `Projects/AI_Core/src/modules/proxmox_manager.py` | Keep if Proxmox automation used. |
| https://100.74.137.122:8006/#v1:0:18:4::::::: | Infra/UI (Proxmox) | `Projects/AI_Core/src/modules/proxmox_manager.py` | Keep if Proxmox automation used. |
| https://192.168.190.126/ | Infra/UI (Proxmox) | `Projects/AI_Core/src/modules/proxmox_manager.py` | Keep if Proxmox automation used. |
| https://console.cloud.google.com/billing/011CFE-33CC55-CEFB8F/reports;chartType=STACKED_AREA;timeRange=CUSTOM_RANGE;from=2025-12-01;to=2025-12-31;grouping=GROUP_BY_SKU;skus=services%2FE505-1604-58F8%2Fskus%2F8463-DF87-CC7B | Portal/Docs | GCP APIs used | Optional billing analysis. |
| https://claude.ai/new | Portal/Docs | Anthropic in code: `Projects/AI_Core/src/inference_client.py` | Optional UI. |
| https://100.78.145.67:8006/#v1:0:=node%2Fpve:4::::::: | Infra/UI (Proxmox) | `Projects/AI_Core/src/modules/proxmox_manager.py` | Keep if Proxmox automation used. |
| https://mail.yandex.ru/?ncrnd=48501&uid=1395655937#/tabs/relevant?current_folder=1 | Portal/Docs | Not directly integrated | Optional/manual. |
| https://openrouter.ai/settings/keys | In code | `Projects/AI_Core/src/inference_client.py`, `Projects/Content_Factory/src/pipeline/vibranium_creativity.py` | Keep if OpenRouter used. |
| https://app.electricitymaps.com/dashboard | Not found | No repo references | Optional/manual. |
| https://dialogs.yandex.ru/developer | In code (Yandex Alice) | `Projects/AI_Core/src/alice_skill.py`, `Scripts/automation/start_alice_tunnel.sh` | Keep if Alice skill used. |
| https://www.linkedin.com/feed/ | Not found | No repo references | Optional/personal. |
| https://console.cloud.google.com/monitoring/integrations?project=my-home-435112&pageState=(%22integrations%22:(%22p%22:5)) | Portal/Docs | `Scripts/monitoring/metrics_collector.py` | Keep if metrics to GCP. |
| https://console.cloud.google.com/billing/011CFE-33CC55-CEFB8F/reports?project=gen-lang-client-0982257437 | Portal/Docs | GCP APIs used | Optional billing analysis. |
| http://localhost:3000/ | Infra/UI (local app) | Not referenced directly | Optional; map to actual local service if needed. |
| https://my.edu.gov.il/my-courses | Not found | No repo references | Optional/personal. |
| https://parents.education.gov.il/prhnet/my-children | Not found | No repo references | Optional/personal. |
| https://psagot.edu-haifa.org.il/ | Not found | No repo references | Optional/personal. |
| https://notebooklm.google.com/notebook/147baabe-24a6-40ae-b552-1c12e911c0e0?artifactId=63cdfd0d-5f5f-40ee-a54d-dc515461aed0&pli=1 | Not found | No repo references | Optional/manual. |
| https://www.pexels.com/ru-ru/api/key/ | In code | `Projects/Content_Factory/src/pipeline/pexels_broll.py`, `Projects/Content_Factory/src/researcher/daily_researcher.py` | Keep if Pexels used. |
| https://dev.runwayml.com/organization/1f3b4847-54ab-4e89-aeca-31aa8861db28/api-keys | In code | `Projects/Content_Factory/src/video/ai_video_generator.py` | Activate if you want Runway video gen. |
| https://app.runwayml.com/video-tools/teams/gonya90gg/dashboard | In code | `Projects/Content_Factory/src/video/ai_video_generator.py` | Activate if you want Runway video gen. |
| https://dream-machine.lumalabs.ai/board/new | In code | `Projects/Content_Factory/src/video/ai_video_generator.py` | Activate if you want Luma video gen. |
| https://dream-machine.lumalabs.ai/account | In code | `Projects/Content_Factory/src/video/ai_video_generator.py` | Activate if you want Luma video gen. |
| https://elevenlabs.io/app/home | In code | `Projects/Content_Factory/src/pipeline/orchestrator_v3_no_face.py`, `Projects/Content_Factory/src/pipeline/orchestrator_v4_advanced.py` | Keep (TTS). |
| https://suno.com/ | In code | `Projects/Content_Factory/src/audio/suno_client.py`, `Projects/Content_Factory/src/audio/music_generator.py` | Activate if you want Suno music gen. |
| https://lumalabs.ai/api/billing/overview | In code | `Projects/Content_Factory/src/video/ai_video_generator.py` | Activate if you want Luma video gen. |
| https://github.com/ | In code | `Projects/AI_Core/src/github_handler.py`, `LLM_Council/council/providers/github_copilot.py` | Keep. |
| https://dream-machine.lumalabs.ai/ | In code | `Projects/Content_Factory/src/video/ai_video_generator.py` | Activate if you want Luma video gen. |
| https://suno.com/@monophonicbootleg242 | In code | `Projects/Content_Factory/src/audio/suno_client.py` | Optional (account mgmt). |
| https://console.cloud.google.com/apis/dashboard?project=my-home-435112&pageState=(%22duration%22:(%22groupValue%22:%22P30D%22,%22customValue%22:null)) | Portal/Docs | GCP APIs used | Optional. |
| https://amproab.adam-milo.co.il/forms?token=... | Not found | No repo references | Optional/personal. |
| https://www.notion.so/profile/integrations | In code | `Projects/AI_Core/src/notion_service.py` | Keep if Notion integration used. |
| https://gonya90gg.atlassian.net/jira/for-you | Not found | No repo references | Optional/personal. |
| https://www.notion.so/profile/integrations/internal/adcb2a9a-b796-44f2-a80d-0d8865c84d6f | In code | `Projects/AI_Core/src/notion_service.py` | Keep if Notion integration used. |
| https://github.com/copilot/spaces/Unified-system-Core/1?tab=attachments | In code (Copilot provider) | `LLM_Council/council/providers/github_copilot.py` | Optional; needed only if using Copilot. |
| https://openclaw.ai/blog/virustotal-partnership | Not found | No repo references | Optional/manual. |
| https://huggingface.co/IgorGYan | In code | `Projects/Content_Factory/src/researcher/daily_researcher.py` | Keep if HF inference used. |

## Activation Opportunities ("Use on Max")

These are already wired in code but require valid keys or explicit enablement.

- Runway video generation: `Projects/Content_Factory/src/video/ai_video_generator.py`
- Luma video generation: `Projects/Content_Factory/src/video/ai_video_generator.py`
- Suno music generation: `Projects/Content_Factory/src/audio/suno_client.py`, `Projects/Content_Factory/src/audio/music_generator.py`
- SerpAPI web search: `Projects/AI_Core/src/web_search.py`, `Scripts/Integrations/serpapi_search.py`
- NVIDIA NIM API: `LLM_Council/council/providers/nvidia_nim.py`
- Hugging Face inference: `Projects/Content_Factory/src/researcher/daily_researcher.py`
- Yandex Alice skill: `Projects/AI_Core/src/alice_skill.py`

## Recommended Cleanup (Only if you do NOT use them)

- Grok, ElectricityMaps, Colab, NotebookLM, LinkedIn, education portals, amproab form, Jira.
- ChatGPT/Gemini UI pages are optional if you only use APIs.

## Next Steps (Pick Priorities)

1. Confirm which of the Activation Opportunities should be turned on first.
2. Provide missing keys/tokens for selected services (or tell me they already exist in TokenBroker).
3. I will enable the integrations and set provider rotation + failover order.
