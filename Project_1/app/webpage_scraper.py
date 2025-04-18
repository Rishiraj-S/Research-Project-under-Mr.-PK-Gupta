import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(filename="scraper.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def scrape_article_content(url):
    """
    Scrapes the main content from a given article URL.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = response.apparent_encoding  # Ensure correct encoding

        if response.status_code != 200:
            logging.warning(f"Failed to fetch {url} (Status Code: {response.status_code})")
            return None, None

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract the title
        title = soup.title.text.strip() if soup.title else "No Title Found"

        # Extract content using multiple approaches
        paragraphs = soup.find_all("p")
        content_divs = soup.find_all(["div", "article"], class_=re.compile("content|article|post|entry"))

        content = " ".join(p.text.strip() for p in paragraphs if p.text.strip())
        if not content and content_divs:
            content = " ".join(div.text.strip() for div in content_divs if div.text.strip())

        return title, content
    
    except Exception as e:
        logging.error(f"Error scraping content from {url}: {e}")
        return None, None

def scrape_ai_articles(company, urls):
    """
    Scrapes AI-related articles from a list of URLs for a given company using multi-threading.
    """
    articles = []

    def process_url(url):
        logging.info(f"Scraping {url} for {company}...")
        title, content = scrape_article_content(url)
        if title and content:
            return {"Company": company, "Title": title, "Content": content, "Link": url}
        return None

    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust number of threads as needed
        results = executor.map(process_url, urls)

    for result in results:
        if result:
            articles.append(result)

    return articles

def get_ai_articles():
    """
    Collects AI-related articles from various IT companies.
    """
    company_websites = {
        "Tata Consultancy Services": [
            "https://www.tcs.com/what-we-do/industries/life-sciences/article/ai-pharma-redefine-drug-development-patient-care",
            "https://www.tcs.com/what-we-do/industries/high-tech/white-paper/generative-ai-hcm-transform-talent-acquisition",
            "https://www.tcs.com/what-we-do/services/iot-digital-engineering/white-paper/generative-ai-software-defined-vehicles",
            "https://www.tcs.com/insights/blogs/generative-ai-hyper-personalized-customer-excellence",
            "https://www.tcs.com/what-we-do/industries/banking/white-paper/iso20022-genai-payments-disruption",
            "https://www.tcs.com/what-we-do/industries/high-tech/white-paper/generative-ai-powered-ebooks-revolutionize-reading",
            "https://www.tcs.com/what-we-do/pace-innovation/article/transform-knowledge-work-generative-ai-augmentation",
            "https://www.tcs.com/who-we-are/events/tcs-interactive-adobe-summit-2025",
            "https://www.tcs.com/what-we-do/industries/communications-media-information-services/white-paper/generative-ai-anomaly-detection-credit-decisioning",
            "https://www.tcs.com/what-we-do/industries/high-tech/white-paper/generative-ai-transforming-application-security-landscape",
            "https://www.tcs.com/who-we-are/newsroom/press-release/tcs-partners-insper-brazil-invests-50mn-accelerate-innovation-south-america",
            "https://www.tcs.com/what-we-do/industries/banking/white-paper/generative-ai-adoption-strategy-bfsi",
            "https://www.tcs.com/what-we-do/industries/banking/article/future-of-genai-bfsi",
            "https://www.tcs.com/what-we-do/services/tcs-interactive/podcast/tcs-talks-tech-season-2",
            "https://www.tcs.com/insights/blogs/generative-ai-sustainable-procurement",
            "https://www.tcs.com/what-we-do/industries/retail/white-paper/generative-ai-retail-customer-experience",
            "https://www.tcs.com/what-we-do/services/artificial-intelligence/white-paper/generative-ai-smart-sales-marketing",
            "https://www.tcs.com/insights/blogs/generative-ai-low-code-no-code-platforms",
            "https://www.tcs.com/what-we-do/industries/banking/white-paper/genai-exceptional-customer-service",
            "https://www.tcs.com/what-we-do/industries/high-tech/white-paper/generative-ai-reimagine-future-product-development",
            "https://www.tcs.com/who-we-are/newsroom/analyst-reports/tcs-recognized-leader-capital-markets-it-services-everest-group",
            "https://www.tcs.com/insights/blogs/generative-ai-future-automotive-marketing",
            "https://www.tcs.com/who-we-are/newsroom/analyst-reports/convergence-private-5G-wi-fi-6-propel-new-enterprise-private-network",
            "https://www.tcs.com/what-we-do/services/iot-digital-engineering/white-paper/digital-thread-generative-ai-intelligent-insights",
            "https://www.tcs.com/what-we-do/industries/capital-markets/white-paper/generative-ai-wealth-management",
            "https://www.tcs.com/insights/blogs/generative-ai-mainframe-modernization",
            "https://www.tcs.com/what-we-do/services/iot-digital-engineering/white-paper/four-tech-mega-trends-iot-edge",
            "https://www.tcs.com/insights/blogs/generative-ai-mainframe-modernization",
            "https://www.tcs.com/what-we-do/industries/capital-markets/white-paper/enterprise-generative-ai-capital-markets",
            "https://www.tcs.com/what-we-do/products-platforms/tcs-add/white-paper/advancing-regulatory-intelligence-with-conversational-generative-ai",
            "https://www.tcs.com/contact-us/product-overlay/talk-to-an-expert-tcs-add/white-paper/advancing-regulatory-intelligence-with-conversational-generative-ai-form",
            "https://www.tcs.com/what-we-do/industries/manufacturing/genai-manufacturing-value-chain",
            "https://www.tcs.com/what-we-do/services/cloud/aws/solution/creating-generative-ai-enabled-enterprise",
            "https://www.tcs.com/what-we-do/industries/communications-media-information-services/article/tcs-tm-forum-knowledge-report",
            "https://www.tcs.com/who-we-are/events/tcs-brazil-bronze-sponsor-exposibram",
            "https://www.tcs.com/who-we-are/worldwide/tcs-na/working-towards-the-future",
            "https://www.tcs.com/who-we-are/events/tcs-life-sciences-forum-2024",
            "https://www.tcs.com/insights/blogs/generative-ai-financial-planning-analysis",
            "https://www.tcs.com/what-we-do/industries/travel-and-logistics/blog/generative-ai-mro",
            "https://www.tcs.com/contact-us/industry-overlay/talk-to-an-expert-life-sciences/article/generative-ai-digital-twin-technology-transforming-life-sciences-form",
            "https://www.tcs.com/what-we-do/industries/life-sciences/article/generative-ai-digital-twin-technology-transforming-life-sciences",
            "https://www.tcs.com/who-we-are/newsroom/press-release/xerox-signs-deal-with-tcs-transform-it-technology-using-cloud-genai",
            "https://www.tcs.com/what-we-do/services/cybersecurity/white-paper/derisking-ai-models-cybersecurity-strategies",
            "https://www.tcs.com/who-we-are/newsroom/press-release/tcs-launches-wisdomnext-an-industry-first-genai-aggregation-platform",
            "https://www.tcs.com/what-we-do/services/artificial-intelligence/solution/enterprise-generative-ai-adoption-wisdomnext",
            "https://www.tcs.com/what-we-do/industries/manufacturing/white-paper/next-gen-technologies-ai-future-mobility",
            "https://www.tcs.com/what-we-do/services/enterprise-solutions/white-paper/generative-ai-human-resources",
            "https://www.tcs.com/what-we-do/industries/high-tech/white-paper/generative-ai-powered-next-generation-semiconductors",
            "https://www.tcs.com/what-we-do/industries/manufacturing/blog/gen-ai-manufacturing-innovation-business-transformation",
            "https://www.tcs.com/what-we-do/industries/communications-media-information-services/white-paper/generative-ai-powered-next-gen-telcos",
            "https://www.tcs.com/who-we-are/newsroom/press-release/tcs-aws-sign-strategic-agreement-accelerate-cloud-transformations-offer-access-genai-solutions-customers",
            "https://www.tcs.com/what-we-do/industries/retail/white-paper/generative-ai-retail-myths-cautions",
            "https://www.tcs.com/insights/topics/ai/blog/generative-ai-models-buy-build-davos",
            "https://www.tcs.com/what-we-do/pace-innovation/article/generative-ai-knowledge-driven-enterprise",
            "https://www.tcs.com/what-we-do/industries/banking/white-paper/generative-ai-finance-balance-sheet-management",
            "https://www.tcs.com/insights/blogs/telcos-csps-sustainable-workplace-culture",
            "https://www.tcs.com/insights/blogs/generative-ai-capital-markets",
            "https://www.tcs.com/what-we-do/pace-innovation/article/generative-ai-guardrails-secure-llm-usage",
        ],
        "Infosys": [
            "https://www.infosys.com/services/application-modernization/analyst-reports/services-solutions-us-2024.html",
            "https://www.infosys.com/iki/perspectives/generative-ai-power-code-migration.html",
            "https://www.infosys.com/iki/videos/ai-public-sector-innovation.html",
            "https://www.infosys.com/newsroom/events/2024/quality-engineering.html",
            "https://www.infosys.com/newsroom/events/2024/ai-first-quality-engineering.html",
            "https://www.infosys.com/industries/healthcare.html",
            "https://www.infosys.com/services/quality-engineering/alliances.html",
            "https://www.infosys.com/services/cloud-cobalt/insights/reimagine-business-enterprise.html",
            "https://www.infosys.com/services/application-modernization/insights/decoding-application-modernization.html",
            "https://www.infosys.com/newsroom/events/2024/servicenow-knowledge-2024.html",
            "https://www.infosys.com/iki/techcompass/digital-channels.html",
            "https://www.infosys.com/services/digital-workplace-services/insights/dws-spotlight/experience-design.html",
            "https://www.infosys.com/iki/techcompass/green-energy.html",
            "https://www.infosys.com/newsroom/events/2025/ai-work-summit-2025.html",
            "https://www.infosys.com/de/newsroom/press-releases/2025/infosys-siemens-digitales-lernen-generative-ki.html",
            "https://www.infosys.com/de/newsroom/press-releases/2025/infosys-siemens-digitales-lernen-generative-ki.html",
            "https://www.infosys.com/de/newsroom/press-releases/2025/infosys-generative-ai-australian-open.html",
            "https://www.infosys.com/newsroom/events/2025/shaping-future-digital-experience-ai-era.html",
            "https://www.infosys.com/newsroom/events/2025/sap-ai-conclave2025.html",
            "https://www.infosys.com/newsroom/events/2025/revolutionizing-application-modernization-ai.html",
            "https://www.infosys.com/newsroom/events/2024/european-news-media-conference.html",
            "https://www.infosys.com/newsroom/events/2024/alteryx-inspire-2024.html",
            "https://www.infosys.com/newsroom/events/2024/mongodb-local-nyc-2024.html",
            "https://www.infosys.com/newsroom/events/2024/world-tour-2024.html",
            "https://www.infosys.com/newsroom/events/2024/focused-ai-conversation.html",
            "https://www.infosys.com/iki/techcompass/fundamental-limitations-solutions.html",
            "https://www.infosys.com/newsroom/events/2025/servicenow-knowledge-2025.html",
            "https://www.infosys.com/iki/techcompass/ai-driven-augmentations.html",
            "https://www.infosys.com/iki/perspectives/ai-drive-transformation-telecoms.html",
            "https://www.infosys.com/newsroom/events/2024/ai-financial-services.html",
            "https://www.infosys.com/iki/perspectives/generative-ai-supply-chain-management.html",
            "https://www.infosys.com/newsroom/events/2024/ai-conversations.html",
            "https://www.infosys.com/newsroom/events/2024/hpe-discover-2024.html",
            "https://www.infosys.com/services/experience-transformation/insights/genai-powered-solutions.html",
            "https://www.infosys.com/iki/events/scaling-genai-future-work.html",
            "https://www.infosys.com/services/experience-transformation/insights/genai-additions-servicenow.html",
            "https://www.infosys.com/services/oracle/insights/complexities-of-genai.html",
            "https://www.infosys.com/services/data-ai-topaz/case-studies/knowledge-enterprise-genai.html",
            "https://www.infosys.com/services/consulting/building-gen-ai.html",
            "https://www.infosys.com/services/quality-engineering/insights/charting-new-horizons.html",
            "https://www.infosys.com/services/experience-transformation/insights/charting-unrivaled-success.html",
            "https://www.infosys.com/services/consulting/shipping-logistics.html",
            "https://www.infosys.com/iki/videos/generative-ai-telecom-innovation.html",
            "https://www.infosys.com/services/consulting/revolutionizing-credit.html",
            "https://www.infosys.com/newsroom/events/2025/financial-services-enterprises-consent.html",
            "https://www.infosys.com/iki/podcasts/ahead-cloud/generative-ai-telecom-network-innovation.html",
            "https://www.infosys.com/industries/consumer-packaged-goods/insights/generative-ai-bubble.html",
            "https://www.infosys.com/services/quality-engineering/insights/transforming-qe.html",
            "https://www.infosys.com/services/data-ai-topaz/case-studies/solving-real-world-poblems.html",
            "https://www.infosys.com/iki/events/scaling-generative-ai.html",
            "https://www.infosys.com/services/quality-engineering/insights/optimize-cloud-migration.html",
            "https://www.infosys.com/products-and-platforms/wingspan/insights/bridging-the-skill.html",
            "https://www.infosys.com/newsroom/press-releases/2023/generate-value-generative-ai.html",
            "https://www.infosys.com/newsroom/press-releases/2023/generative-ai-creates-enterprise-agility.html",
            "https://www.infosys.com/newsroom/press-releases/2024/generative-ai-radar-apac-report2024.html",
            "https://www.infosys.com/newsroom/features/2024/leader-hfs-horizons-generative-enterprise-services.html",
            "https://www.infosys.com/services/data-analytics/insights/generative-enterprises-services.html",
            "https://www.infosys.com/services/cloud-cobalt/offerings/ai-infrastructure.html",
            "https://www.infosys.com/services/salesforce/insights/ai-driven-salesforce-innovations.html",
            "https://www.infosys.com/services/experience-transformation/insights/strategic-partnership.html",
            "https://www.infosys.com/services/cyber-security/insights/data-privacy-protection-overview.html",
            "https://www.infosys.com/newsroom/events/2024/forum-dtw-2024.html",
            "https://www.infosys.com/services/agile-devops/insights/cloud-transformation-devops.html",
            "https://www.infosys.com/services/consulting/strategic-ai.html",
            "https://www.infosys.com/newsroom/events/2024/api-summit-2024.html",
            "https://www.infosys.com/services/quality-engineering/recognitions/quality-engineering-neat-report.html",
            "https://www.infosys.com/services/generative-ai.html",
            "https://www.infosys.com/newsroom/events/2024/insuretech-connect-2024.html",
            "https://www.infosys.com/industries/financial-services/industry-offerings/alert-solutions-dispute-prediction.html",
            "https://www.infosys.com/iki/techcompass/security-threat-resposne.html",
            "https://www.infosys.com/iki/events/operationalizing-generative-ai-enterprise.html",
            "https://www.infosys.com/services/consulting/next-digital-era-overview.html",
            "https://www.infosys.com/services/salesforce/recognitions/ecosystem-partners.html",
            "https://www.infosys.com/services/data-analytics/offerings/databricks-capabilities.html",
            "https://www.infosys.com/services/consulting/offerings/ai-experience.html",
        ],
        "HCLTech": [
            "https://www.hcltech.com/ai",
            "https://www.hcltech.com/digital-business/data-and-ai",
            "https://www.hcltech.com/press-release",
            "https://www.hcltech.com/trends-and-insights/ai"
            "https://www.hcltech.com/geo-presence/singapore?source=Nzc4ODg5-1742886419399",
            "http://hcltech.com/case-study/genai-powered-sentiment-analyzer-reduces-manual-effort-by-70-percent?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/hcltech-advantage-experience-powered-genai?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/hcltech-ai-force?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/hcltech-genai-powered-netops-solution?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/hcltech-and-oracle-ai-solution?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/hcltech-genai-infused-scm-solution?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/hcltech-almate-application-lifecycle-management-solution?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/red-hat-powered-cognitive-infrastructure-services?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/hcltech-intelligence-assist?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/cognitive-infrastructure-services-transforming-enterprises?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/cognitive-infrastructure-services-powered-hpe?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/hcltech-smart-recruit?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/redefine-cognitive-intelligent-operational-excellence-with-hcltech-iona?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/cognitive-infrastructure-services-in-collaboration-with-cisco?source=Nzc4ODg5-1742886419399",
            "http://hcltech.com/brochures/hcltech-code-mentor?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brochures/hcltechs-rapid-analytics-solution?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/analyst/analyst-reports/hcltech-drives-business-ops-and-experience-live-genai?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/analyst-reports/hcltech-ai-force-scalable-modular-and-backed-proven-ai-expertise?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/analyst-reports/reliable-proven-and-high-functioning-hcltech-cloud-native-and-genai-labs?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brand/hcltech-ai-pc?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-launches-ai-force-accelerate-time-value-software-development-and-engineering?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/brand/ai-genai-hcltech?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-launches-strategic-initiative-google-cloud-scale-gemini-global-enterprises?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-integrates-its-genai-platform-hcltech-ai-forcetm-google-gemini?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-launches-enterprise-ai-foundry-drive-ai-effectiveness-across-enterprise?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/corporate/hcltech-will-focus-genai-led-solutions-client-demand-ceo-c-vijayakumar?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-and-microsoft-expand-collaboration-boost-innovation-and-adoption-generative?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-launches-suite-salesforce-based-solutions-advance-genai-capabilities-across?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-infuses-genai-mro-solution-redefine-enterprises-asset-utilization?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/hcltech-ai-powered-clinical-advisor?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/hcltechs-office-ai-secure-ethical-and-responsible-ai-implementation?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/hcltech-ai-force-accelerated-nvidia-ai-enterprise?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-and-ibm-announce-genai-center-excellence-support-clients-customized-ai?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-and-servicenow-partner-deliver-genai-led-solutions?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-collaborates-sap-boost-innovation-and-adoption-generative-ai?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-collaborates-aws-accelerate-genai-adoption?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-study-reveals-access-emerging-technologies-and-improved-security-are-driving?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-and-microsoft-partner-cricket-australia-transform-fan-experience-genai?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/newsfeed/hcltech-launches-enterprise-ai-foundry-microsoft-azure?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/press-releases/hcltech-and-aws-enter-strategic-collaboration-accelerate-genai-adoption?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/newsfeed/hcltech-partners-multiverse-upskill-uk-employees-ai-and-genai?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/hcltech-smarttwin-solution?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/blogs/manufacturing-companies-get-a-genai-boost-with-hcltech-insight?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/transform-your-business-with-cutting-edge-gen-ai-solutions?source=NzUyNTYx-1742885500692",
            "https://www.hcltech.com/genai-in-cybersecurity?source=NzUyNTYx-1742885500692",
            "https://www.hcltech.com/scale-ai?source=NzUyNTYx-1742885500692",
            "https://www.hcltech.com/cognitive-ai-knowledge-assistant-for-enterprises?source=NzUyNTYx-1742885500692",
            "https://www.hcltech.com/data-and-ai?source=NzUyNTYx-1742885500692",
            "https://www.hcltech.com/newsfeed/hcltech-enhances-digital-experience-solution-genai-transform-marketing-and-customer?source=NzUyNTYx-1742885500692",
            "https://www.hcltech.com/generative-ai-services?source=NzUyNTYx-1742885500692",
            "https://www.hcltech.com/datagenie-synthetic-data-generation?source=NzUyNTYx-1742885500692",
            "https://www.hcltech.com/case-study/genai-powered-sentiment-analyzer-reduces-manual-effort-by-70-percent",
            "https://www.hcltech.com/case-study/effective-pharma-compliance-with-genai",
            "https://www.hcltech.com/white-papers/generative-ai-amplifies-the-need-for-financial-services-to-accelerate-cloud-adoption",
            "https://www.hcltech.com/white-papers/challenges-in-genai-adoption?source=Nzc4ODg5-1742885633578",
            "https://www.hcltech.com/white-papers/making-the-right-decision?source=Nzc4ODg5-1742885633578",
            "https://www.hcltech.com/brochures/hcltech-citizen-advisor?source=Nzc4ODg5-1742885633578",
            "https://www.hcltech.com/brochures/hcltech-intelligent-content-studio?source=Nzc4ODg5-1742885633578",
            "https://www.hcltech.com/brochures/hcltech-advantage-experience-powered-genai?source=Nzc4ODg5-1742885633578",
            "https://www.hcltech.com/campaign/smart-lab?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/ai-force?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/newsfeed/hcltech-enhances-digital-experience-solution-genai-transform-marketing-and-customer?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/scale-ai?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/responsible-ai?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/accelerate-high-performance-computing-adoption?source=Nzc4ODg5-1742886419399",
            "https://www.hcltech.com/newsfeed/hcltech-launches-salesforce-based-solutions-advanced-genai-and-data-capabilities-enhanced?source=Nzc4ODg5-1742886419399",
        ],
        "Wipro": [
            "https://www.wipro.com/cloud/joint-report-with-forbes-how-to-master-cloud-economics-and-harness-the-power-of-ai/",
            "https://www.wipro.com/ai/",
            "https://www.wipro.com/case-studies/"
            "https://www.wipro.com/ai/unlock-the-power-of-ai-to-drive-enterprise-business-transformation/",
            "https://www.wipro.com/analyst-speak/wipro-named-a-leader-in-everest-groups-quality-engineering-services-for-ai-applications-and-systems-peak-matrix-assessment-for-2024/",
            "https://www.wipro.com/analyst-speak/wipro-highlighted-as-a-product-leader-in-gartner-2024-emerging-tech-services-innovation-using-ai-technologies/",
            "https://www.wipro.com/analyst-speak/building-digital-era-ai-first-intelligent-enterprises-spotlighted-as-market-leader-in-hfs-horizons-generative-enterprise-services-2023/",
            "https://www.wipro.com/ai/wega-studio/",
            "https://www.wipro.com/capital-markets/wealthai/",
            "https://www.wipro.com/ai/inspectai/",
            "https://www.wipro.com/ai/sovereign-ai/",
            "https://www.wipro.com/ai/services/agentic-ai/",
            "https://www.wipro.com/cloud/articles/driving-business-outcomes-with-ai/",
            "https://www.wipro.com/cloud/articles/how-ai-and-industry-cloud-combine-to-accelerate-innovation-and-power-business-value/",
            "https://www.wipro.com/blogs/sandhya-arun/from-genai-to-roi-six-simple-steps-to-derive-maximum-value-from-genai-at-enterprise-scale/"
        ],
        "Cognizant": [
            "https://www.cognizant.com/us/en/services/ai/generative-ai",
            "https://www.cognizant.com/us/en/insights/tech-to-watch/generative-ai",
            "https://www.cognizant.com/us/en/services/cloud-solutions/aws-cloud/generative-ai-solutions",
            "https://www.cognizant.com/us/en/services/neuro-intelligent-automation/neuro-generative-ai-adoption",
            "https://www.cognizant.com/us/en/aem-i/generative-ai-future-of-work",
            "https://www.cognizant.com/us/en/aem-i/generative-ai-economic-model-oxford-economics",
            "https://www.cognizant.com/us/en/services/ai",
            "https://www.cognizant.com/us/en/services/ai/ai-lab",
            "https://www.cognizant.com/us/en/services/software-engineering-services/flowsource",
            "https://www.cognizant.com/us/en/services/ai/ai-solutions",
            "https://www.cognizant.com/us/en/campaigns/generative-ai-actionable-consumer-strategies-ebook",
            "https://www.cognizant.com/us/en/services/ai/generative-ai-handbook",
            "https://www.cognizant.com/us/en/cmp/starbucks",
            "https://www.cognizant.com/us/en/insights/insights-blog/generative-ai-societys-new-equalizer-wf2369113",
            "https://www.cognizant.com/us/en/about-cognizant/sustainability-corporate-citizenship/synapse",
            "https://www.cognizant.com/us/en/insights/insights-blog/generative-ai-productivity-wf2343151",
            "https://www.cognizant.com/us/en/insights/insights-blog/how-gen-ai-will-forever-change-data-engineering-wf1807301",
            "https://www.cognizant.com/us/en/campaigns/realising-the-real-business-impact-of-generative-ai",
            "https://www.cognizant.com/us/en/services/ai/rewire-for-ai",
            "https://www.cognizant.com/us/en/insights/insights-blog/generative-ai-in-the-workforce-wf2343510",
            "https://www.cognizant.com/us/en/insights/insights-blog/generative-ai-for-new-revenue-sources",
            "https://www.cognizant.com/us/en/trizetto/generative-ai-in-healthcare",
            "https://www.cognizant.com/us/en/insights/insights-blog/chatgpt-and-the-generative-ai-revolution-wf1532750",
            "https://www.cognizant.com/us/en/insights/insights-blog/gen-ai-impact-on-women-in-the-workplace-wf2458851",
            "https://www.cognizant.com/us/en/services/business-process-services/ai-business-accelerators",
            "https://www.cognizant.com/us/en/insights/insights-blog/4-ways-clinical-development-will-improve-with-gen-ai-wf1992400",
            "https://www.cognizant.com/us/en/insights/insights-blog/nordics-generative-ai-adoption",
            "https://www.cognizant.com/us/en/insights/insights-blog/gen-ai-strategy-wf2851465",
            "https://www.cognizant.com/us/en/aem-i/new-minds-new-markets-ai-customer-experience",
            "https://www.cognizant.com/us/en/insights/insights-blog/customer-centricity-and-generative-ai",
            "https://www.cognizant.com/us/en/insights/insights-blog/reimagining-csp-field-operations-with-generative-ai-wf2670452",
            "https://www.cognizant.com/us/en/services/enterprise-quality-engineering-assurance/ai-quality-assurance",
            "https://www.cognizant.com/us/en/insights/insights-blog/generative-ai-in-reskilling-and-growth-wf2618204",
            "https://www.cognizant.com/us/en/services/ai/decision-ai",
            "https://www.cognizant.com/us/en/services/ai",
            "https://www.cognizant.com/us/en/cmp/empowering-transformation-transportation-and-logistics",
            "https://www.cognizant.com/us/en/aem-i/gen-ai-impact-on-jobs",
            "https://www.cognizant.com/us/en/aem-i/future-ready-ai",
            "https://www.cognizant.com/us/en/services/neuro-intelligent-automation/neuro-edge-generative-ai",
            "https://www.cognizant.com/us/en/world-economic-forum",
            "https://www.cognizant.com/us/en/services/neuro-intelligent-automation/neuro-ai-it-operations",
            "https://www.cognizant.com/us/en/insights/insights-blog/gen-ai-raises-copyright-issues-could-blockchain-solve-them-wf2372662",
            "https://www.cognizant.com/us/en/insights/insights-blog/gen-ai-is-no-screenwriter-yet-wf1951868",
            "https://www.cognizant.com/us/en/cmp/aws-strategic-partnership-strategic-collaboration-generative-ai",
            "https://www.cognizant.com/us/en/insights/insights-blog/how-gen-ai-can-revolutionize-travel-and-transport-wf2077514",
            "https://www.cognizant.com/us/en/insights/tech-to-watch",
            "https://www.cognizant.com/us/en/services/ai/consulting",
            "https://www.cognizant.com/us/en/cmp/cxvegas",
            "https://www.cognizant.com/us/en/insights/insights-blog/the-impact-of-gen-ai-on-the-new-workforce-wf2785550",
            "https://www.cognizant.com/us/en/insights/insights-blog",
            "https://www.cognizant.com/us/en/case-studies",
            "https://www.cognizant.com/us/en/insights/insights-blog/5-unconventional-truths-for-building-gen-ai-programs-in-biopharma-wf2327093",
            "https://www.cognizant.com/us/en/insights/insights-blog/how-to-execute-a-gen-ai-strategy-wf2465236",
            "https://www.cognizant.com/us/en/insights/insights-blog/get-ready-for-the-gen-ai-skills-shuffle-wf1833251",
            "https://www.cognizant.com/us/en/industries/automotive-technology-solutions",
            "https://www.cognizant.com/us/en/services/intelligent-process-automation",
            "https://www.cognizant.com/us/en/services/neuro-intelligent-automation/neuro-generative-ai-adoption/enterprise-agentic-ai",
            "https://www.cognizant.com/us/en/services/neuro-intelligent-automation/ai-cybersecurity",
            "https://www.cognizant.com/us/en/insights/insights-blog/gen-ai-data-privacy-laws-wf2373254",
            "https://www.cognizant.com/us/en/about-cognizant/responsible-ai",
            "https://www.cognizant.com/us/en/services/business-process-services/ai-training-services",
            "https://www.cognizant.com/us/en/insights/insights-blog/gen-ai-from-theory-to-practice-wf2237000",
            "https://www.cognizant.com/us/en/about-cognizant/partners/google-cloud"],
        "TechMahindra": [
            "https://www.techmahindra.com/insights/news/",
            "https://www.techmahindra.com/services/artificial-intelligence/",
            "https://www.techmahindra.com/insights/whitepapers/transformative-power-genai-reshaping-banking-industry/",
            "https://www.techmahindra.com/insights/events/tech-mahindra-proud-platinum-sponsor-databricks-data-ai-world-tour-zurich/",
            "https://www.techmahindra.com/insights/press-releases/tech-mahindra-announces-integration-with-servicenow-deliver-genai-powered-esm-solution/",
            "https://www.techmahindra.com/insights/press-releases/tech-mahindra-and-aws-collaborate-transform-telecom-networks-generative-ai/",
            "https://www.techmahindra.com/insights/news/new-hfs-research-and-tech-mahindra-report-generative-ai-adoption/",
            "https://www.techmahindra.com/insights/press-releases/tech-mahindra-inks-mou-with-the-open-university/",
            "https://www.techmahindra.com/insights/brochures/empowering-business-datanext-gen-analytics-solutions/",
            "https://www.techmahindra.com/insights/whitepapers/benchmarking-indus-language-model-intel-hardware/",
            "https://www.techmahindra.com/services/integrated-offerings/",
            "https://www.techmahindra.com/insights/views/chaos-clarity-transform-your-data-visualization-visualization-service-vaas/",
            "https://www.techmahindra.com/insights/press-releases/tech-mahindra-collaborates-microsoft-modernize-workplace-experiences-generative-ai/",
            "https://www.techmahindra.com/insights/views/ai-axis-realizing-full-potential-generative-ai-agentx/",
            "https://www.techmahindra.com/insights/case-studies/transforming-healthcare-marketing-ai-powered-precision/",
            "https://www.techmahindra.com/insights/analyst-insights/indus-project-story-co-authored-third-eye-advisory/",
            "https://www.techmahindra.com/insights/press-releases/tech-mahindra-launches-project-indus-large-language-model-llm/",
            "https://www.techmahindra.com/insights/views/future-mobility-generative-ai-genai-integral-capability/",
            "https://www.techmahindra.com/insights/views/moving-past-genai-honeymoon-phase-key-factors-consider-scaling-adoption/",
            "https://www.techmahindra.com/services/techm-consulting/data-and-ai-consulting/",
            "https://www.techmahindra.com/insights/press-releases/tech-mahindra-launches-agentx-comprehensive-suite-genai-solutions/",
            "https://www.techmahindra.com/insights/views/trust-and-safety-age-genai-powered-innovation/",
            "https://www.techmahindra.com/industries/healthcare-life-sciences/pharma/genai-medical-writing/",
            "https://www.techmahindra.com/insights/views/blueprint-enable-successful-genai-adoption-your-enterprise/",
            "https://www.techmahindra.com/insights/case-studies/ensuring-workflow-efficiency-using-genai-reducing-250-person-hoursmonth/",
            "https://www.techmahindra.com/insights/case-studies/tech-mahindra-saved-over-140mn-global-fb-firm-hyper-automation/",
            "https://www.techmahindra.com/insights/events/meet-tech-mahindra-google-cloud-next-2025/",
            "https://www.techmahindra.com/insights/views/future-operational-efficiency-agentx-driving-innovation-enterprise-processes/",
            "https://www.techmahindra.com/services/application-development-maintenance-service/techm-appginiez/",
            "https://www.techmahindra.com/insights/press-releases/tech-mahindra-launches-verifai-comprehensive-genai-validation-solution-enterprises-globally/",
            "https://www.techmahindra.com/insights/events/cxo-roundtable-shaping-future-networks-ai-and-ml-autonomous-operations/",
            "https://www.techmahindra.com/insights/press-releases/tech-mahindra-announces-ai-center-excellence-powered-nvidia-ai-enterprise-and-omniverse/",
            "https://www.techmahindra.com/insights/press-releases/tech-mahindra-and-atento-partner-deliver-genai-powered-business-transformation-services-global/",
            "https://www.techmahindra.com/insights/views/empowering-hi-tech-titans-unleashing-genai-and-cloud-innovations/",
            "https://www.techmahindra.com/insights/events/cxo-roundtable-rise-genai-manufacturing-enterprises/",
            "https://www.techmahindra.com/insights/events/cxo-roundtable-rise-genai-retail-cpg-travel-and-transportation-industry/",
            "https://www.techmahindra.com/insights/views/role-genai-achieving-back-office-efficiency/",
            "https://www.techmahindra.com/insights/views/genai-shift-experimentation-implementation-unlocking-business-potential/",
            "https://www.techmahindra.com/insights/views/vision-value-role-outcome-centric-governance-genai-adoption/",
            "https://www.techmahindra.com/insights/press-releases/tech-mahindra-and-ibm-establish-synergy-lounge-accelerate-digital-adoption-apac/",
            "https://www.techmahindra.com/insights/press-releases/tech-mahindra-and-ibm-help-enterprises-accelerate-adoption-trustworthy-generative-ai-using/",
            "https://www.techmahindra.com/insights/views/harnessing-ai-speed-and-purpose-building-generative-enterprise-future/",
            "https://www.techmahindra.com/insights/views/how-generative-ai-driving-revenue-operations-new-heights/",
            "https://www.techmahindra.com/insights/views/revolutionizing-cloud-services-role-gen-ai-and-ml-cost-effective-delivery/",
            "https://www.techmahindra.com/services/artificial-intelligence/generative-ai/",
            "https://www.techmahindra.com/insights/views/leveraging-agentic-ai-success-large-deals-enhancing-efficiency-and-innovation/",
            "https://www.techmahindra.com/alliance/dell-partnership/",
            "https://www.techmahindra.com/alliance/dell-partnership/",
            "https://www.techmahindra.com/services/business-process-services/our-services/next-gen-service-desk-solutions/",
            "https://www.techmahindra.com/insights/views/generative-ai-paradigm-shift-content-creation-product-development/",
            "https://www.techmahindra.com/alliance/ibm-partnership/",
            "https://www.techmahindra.com/insights/whitepapers/moving-sdlc-ai-driven-software-development-lifecycle-adlc-generate-value/",
            "https://www.techmahindra.com/insights/analyst-insights/implementing-data-security-accelerate-generative-ai-initiatives/",
            "https://www.techmahindra.com/insights/views/workload-automation-understanding-need-it-operations-and-future-trends-rise-aiml/",
        ],
        "LTIMindtree": [
            "https://www.ltimindtree.com/insights/",
            "https://www.ltimindtree.com/news-event/still-early-days-for-genai-on-revenue-side/",
            "https://www.ltimindtree.com/the-generative-ai-revolution/",
            "https://www.ltimindtree.com/enterprise-ai/",
            "https://www.ltimindtree.com/blogs/rasa-and-generative-ai-the-two-pronged-approach-to-building-chatbots/",
            "https://www.ltimindtree.com/news-event/ltimindtree-unveils-navisource-ai/",
            "https://www.ltimindtree.com/news-event/farmers-edge-and-ltimindtree-unveil-feil/",
            "https://www.ltimindtree.com/news-event/ltim-to-deliver-ai-powered-applications-with-microsoft/",
            "https://www.ltimindtree.com/blogs/how-to-accelerate-the-adoption-of-a-transparent-and-adaptable-ai/",
            "https://www.ltimindtree.com/blogs/embracing-the-future-with-generative-ai-operationalizing-large-language-models-using-snowflake-and-aws-sagemaker/",
            "https://www.ltimindtree.com/blogs/the-future-of-generative-ai-from-models-to-emergent-ai/",
            "http://ltimindtree.com/blogs/from-data-to-care-the-impact-of-genai-on-patient-experiences/",
            "https://www.ltimindtree.com/blogs/unifying-data-simplifying-business-decisions-with-ai-genai/",
            "https://www.ltimindtree.com/data-analytics-services/genai-powered-data-fabric-whitepaper/",
            "https://www.ltimindtree.com/services/low-code/applify-ai-unleashing-the-power-of-low-code-development-and-genai/",
            "https://www.ltimindtree.com/exploring-the-future-of-genai-with-snowflake/",
            "https://www.ltimindtree.com/blogs/a-paradigm-shift-in-customer-service-with-generative-ai-genai-making-intelligent-chatbots-to-enhance-customer-support/",
            "https://www.ltimindtree.com/blogs/empowering-market-insights-and-decision-making-with-gen-ai-agentic-workflows/",
            "https://www.ltimindtree.com/news-event/genai-voice-advisor-launched-by-thomas-cook-sotc-ltimindtree-and-partners/",
            "https://www.ltimindtree.com/services/digital-engineering/accelerating-devops-with-ai/",
            "https://www.ltimindtree.com/news-event/ltimindtree-reports-1-8-qoq-5-6-yoy-revenue-growth/",
            "https://www.ltimindtree.com/ai-banking-finance/",
            "https://www.ltimindtree.com/data-analytics-services/databricks-data-intelligent-platform-for-genai-solutions-pov/",
            "https://www.ltimindtree.com/blogs/generative-ai-in-cards-and-payments-ensuring-security-and-streamlining-transactions/",
            "https://www.ltimindtree.com/blogs/ai-for-all-empowering-women-in-tech-through-genai/",
            "https://www.ltimindtree.com/news-event/ltimindtree-launches-ai-driven-cyber-defense-center/",
            "https://www.ltimindtree.com/blogs/ai-in-financial-risk-management-how-generative-ai-is-transforming-risk-and-compliance-in-financial-services/",
            "https://www.ltimindtree.com/digital-interactive-services/marketing-campaigns-and-content-operations/",
            "https://www.ltimindtree.com/industries/insurance/",
            "https://www.ltimindtree.com/news-event/ltim-delivers-2-8-qoq-usd-revenue-growth/",
            "https://www.ltimindtree.com/blogs/enhancing-agile-delivery-with-generative-ai/",
            "https://www.ltimindtree.com/enterprise-ai/gen-ai-adoption-report/",
            "https://www.ltimindtree.com/blogs/databricks-summit-2024-leading-the-charge-in-data-and-ai-innovation/",
            "https://www.ltimindtree.com/news-event/ltim-and-snowflake-boost-ai-adoption/",
            "https://www.ltimindtree.com/industries/insurance/leapfrog/"
        ],
        "Dell":[
            "https://www.dell.com/en-in/shop/scc/sc/artificial-intelligence#ai-factory-dell",
            "https://www.dell.com/en-in/shop/poweredge-ai-servers/sf/poweredge-ai-servers?hve=explore+servers+for+ai",
            "https://www.dell.com/en-in/lp/dt/ai-technologies",
            "https://www.dell.com/en-in/dt/solutions/artificial-intelligence/storage-for-ai.htm?hve=explore+storage+for+ai#tab0=0",
            "https://www.dell.com/en-in/dt/networking/index.htm?hve=explore+networking+for+ai#tab0=0",
            "https://www.dell.com/en-in/dt/what-we-do/emerging-technology/data-management.htm?hve=explore+data+management+for+ai#tab0=0&tab1=0",
            "https://www.dell.com/en-in/lp/data-protection-ai?hve=explore+data+protection+for+ai",
            "https://www.dell.com/en-in/shop/scc/sc/artificial-intelligence#ai-factory-dell",
            "https://www.dell.com/en-in/lp/dt/artificial-intelligence-services",
        ]
    }
    
    all_articles = []
    
    for company, urls in company_websites.items():
        articles = scrape_ai_articles(company, urls)
        all_articles.extend(articles)
    
    return pd.DataFrame(all_articles)

if __name__ == "__main__":
    df = get_ai_articles()
    if not df.empty:
        df.to_csv("data/genai_company_articles.csv", index=False)
        print("Scraped data saved to genai_company_articles.csv")
    else:
        print("No articles found. Check the website structures or try different keywords.")
