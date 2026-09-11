"""
Submiq synthetic dataset generator.

Produces data/raw/submiq_dataset.csv from a hard-coded, hand-labeled list of
example onboarding submissions covering ten scenario categories, with many
domain-varied examples per category (software, data, design, marketing,
sales, healthcare, education, finance, support, ops, legal, logistics,
hospitality, and more) so no module can overfit to a single writing style
or industry.

Labels are independent per dimension so each of the five Submiq modules —
and the aggregator — can be evaluated separately.

Run:  python generate_synthetic_dataset.py
"""

import csv
import random
from pathlib import Path

random.seed(42)  # fixed seed — required for reproducibility (Sec 3.2.2)

OUT_PATH = Path(__file__).parent / "submiq_dataset.csv"

FIELDS = [
    "submission_id", "scenario_category", "experience_level", "skills",
    "bio", "questionnaire_response", "source",
    "completeness_label", "text_quality_label",
    "plausibility_label", "consistency_label", "expected_verdict",
]

EXAMPLES = [

    # ======================================================================
    # 1. COMPLETE, GENUINE-LOOKING (HUMAN)  -- 12 examples
    # ======================================================================
    dict(scenario_category="Complete, genuine (human)", experience_level="Intermediate",
         skills="React, Node.js, PostgreSQL",
         bio="I've spent the last four years building web applications for small "
             "businesses, mostly e-commerce sites and internal tooling. I like "
             "working close to the metal on performance issues, but I've also led "
             "a small team through a full product rewrite last year.",
         questionnaire_response="Recently migrated a legacy PHP monolith to a "
             "Node/React stack over six months, cutting page load time by 40%.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Complete, genuine (human)", experience_level="Expert",
         skills="Python, Django, AWS, Docker",
         bio="Backend engineer with eight years of experience, primarily in "
             "fintech. I've designed and scaled payment processing systems "
             "handling several thousand transactions per minute, and mentored "
             "junior engineers on system design.",
         questionnaire_response="Led the migration of our payments service from "
             "a monolith to microservices, reducing deployment time from hours "
             "to minutes.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Complete, genuine (human)", experience_level="Entry",
         skills="HTML, CSS, JavaScript",
         bio="I just finished a six-month coding bootcamp and built three "
             "portfolio projects, including a budgeting app and a recipe "
             "sharing site. I'm eager to learn from a real engineering team.",
         questionnaire_response="Built a personal budgeting app using vanilla "
             "JavaScript and localStorage as my capstone project.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Complete, genuine (human)", experience_level="Intermediate",
         skills="Figma, User Research, Prototyping",
         bio="Product designer with five years of experience, mostly on B2B "
             "SaaS dashboards. I run my own usability sessions and work "
             "closely with engineering to make sure designs actually ship as "
             "intended, not just look good in Figma.",
         questionnaire_response="Redesigned our onboarding flow after running "
             "eight user interviews, which raised activation rate from 52% to "
             "61% over one quarter.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Complete, genuine (human)", experience_level="Intermediate",
         skills="Google Analytics, SEO, Paid Search",
         bio="Marketing analyst who has spent the past three years split "
             "between SEO and paid acquisition for a mid-size retail brand. "
             "I'm comfortable pulling my own data and building dashboards, "
             "not just handing reporting off to someone else.",
         questionnaire_response="Ran an A/B test on landing page copy that "
             "improved conversion rate from 2.1% to 2.6%, which we rolled out "
             "site-wide.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Complete, genuine (human)", experience_level="Expert",
         skills="Kubernetes, Terraform, CI/CD, AWS",
         bio="DevOps engineer with seven years of experience, the last three "
             "focused entirely on Kubernetes infrastructure for a company "
             "running around 200 microservices. I care a lot about making "
             "on-call less painful for everyone else on the team.",
         questionnaire_response="Rebuilt our CI/CD pipeline with Terraform "
             "and GitHub Actions, cutting average deploy time from 25 minutes "
             "to under 6.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Complete, genuine (human)", experience_level="Intermediate",
         skills="Patient Scheduling, EHR Systems, Medical Billing",
         bio="I've worked as a clinic administrator for four years at a "
             "family practice, handling scheduling, insurance verification, "
             "and EHR data entry. I trained two new front-desk hires last "
             "year on our intake process.",
         questionnaire_response="Reduced patient check-in time by "
             "reorganizing our EHR intake form to cut redundant fields.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Complete, genuine (human)", experience_level="Intermediate",
         skills="Legal Research, Document Review, Westlaw",
         bio="I've worked as a paralegal at a small litigation firm for "
             "four years, mostly on discovery and document review for "
             "commercial disputes. I've also drafted first-pass motions "
             "for attorney review.",
         questionnaire_response="Managed document review for a case "
             "involving roughly 40,000 documents, building a tagging system "
             "that cut attorney review time significantly.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Complete, genuine (human)", experience_level="Intermediate",
         skills="Inventory Management, Forklift Certified, WMS Software",
         bio="I've worked in warehouse operations for five years, the last "
             "two as a shift lead coordinating a team of eight. I'm "
             "comfortable with our WMS software and have helped train new "
             "hires on safety procedures.",
         questionnaire_response="Reorganized our pick paths in the "
             "warehouse, cutting average order fulfillment time by about "
             "15%.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Complete, genuine (human)", experience_level="Intermediate",
         skills="Swift, iOS Development, Xcode",
         bio="iOS developer with four years of experience building and "
             "maintaining consumer apps. I've shipped two apps to the App "
             "Store from scratch and currently maintain a codebase with "
             "around 200,000 monthly active users.",
         questionnaire_response="Rebuilt our app's onboarding flow in "
             "SwiftUI, reducing crash rate on first launch from 3% to under "
             "0.5%.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Complete, genuine (human)", experience_level="Intermediate",
         skills="Animal Handling, Veterinary Software, Client Communication",
         bio="I've worked as a veterinary technician for six years at a "
             "small-animal clinic, assisting with surgery prep, lab work, "
             "and client education. I'm certified in animal CPR and "
             "comfortable handling emergency cases.",
         questionnaire_response="Helped implement a new digital record "
             "system that cut appointment check-in time roughly in half.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Complete, genuine (human)", experience_level="Intermediate",
         skills="Calendar Management, Travel Coordination, Confidentiality",
         bio="I've worked as an executive assistant supporting a VP-level "
             "team for three years, managing complex calendars across three "
             "time zones and coordinating international travel. I'm used to "
             "handling sensitive information with discretion.",
         questionnaire_response="Reorganized the executive's meeting "
             "structure, cutting weekly calendar conflicts from several per "
             "week to almost none.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),

    # ======================================================================
    # 2. INCOMPLETE  -- 12 examples
    # ======================================================================
    dict(scenario_category="Incomplete", experience_level="Intermediate",
         skills="Java",
         bio="Software developer.",
         questionnaire_response="",
         source="Human", completeness_label="No", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Incomplete", experience_level="",
         skills="Figma, Sketch",
         bio="I design things.",
         questionnaire_response="N/A",
         source="Human", completeness_label="No", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Incomplete", experience_level="Expert",
         skills="",
         bio="TBD, will fill in later.",
         questionnaire_response="",
         source="Human", completeness_label="No", text_quality_label="Poor",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Incomplete", experience_level="Entry",
         skills="Sales",
         bio="Looking for a sales role.",
         questionnaire_response="",
         source="Human", completeness_label="No", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Incomplete", experience_level="Intermediate",
         skills="",
         bio="Data analyst with experience in reporting.",
         questionnaire_response="Not sure what to put here.",
         source="Human", completeness_label="No", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Incomplete", experience_level="Entry",
         skills="QA testing",
         bio="",
         questionnaire_response="I test software for bugs.",
         source="Human", completeness_label="No", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Incomplete", experience_level="Intermediate",
         skills="Operations, Logistics",
         bio="Ops person, will add more details soon.",
         questionnaire_response="Skip for now.",
         source="Human", completeness_label="No", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Incomplete", experience_level="Entry",
         skills="",
         bio="Server at a restaurant for two years.",
         questionnaire_response="",
         source="Human", completeness_label="No", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Incomplete", experience_level="",
         skills="Troubleshooting, Windows, Networking",
         bio="IT support, ask me anything.",
         questionnaire_response="",
         source="Human", completeness_label="No", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Incomplete", experience_level="Intermediate",
         skills="Photography",
         bio="I'm a photographer.",
         questionnaire_response="See portfolio (not attached).",
         source="Human", completeness_label="No", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Incomplete", experience_level="Entry",
         skills="",
         bio="",
         questionnaire_response="Insurance claims processing.",
         source="Human", completeness_label="No", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Incomplete", experience_level="Intermediate",
         skills="Personal Training",
         bio="Been a trainer for a while, will update this section later.",
         questionnaire_response="N/A for now",
         source="Human", completeness_label="No", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),

    # ======================================================================
    # 3. POOR-QUALITY WRITING  -- 12 examples
    # ======================================================================
    dict(scenario_category="Poor-quality writing", experience_level="Intermediate",
         skills="marketing, social media, content",
         bio="i do marketing stuff for like 3 years now and im good at social "
             "media and also content and other things like that basically "
             "im good at marketing in general u know",
         questionnaire_response="i made posts that got alot of likes for a "
             "brand once",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Poor-quality writing", experience_level="Entry",
         skills="excel, data entry",
         bio="good with numbers and spredsheets have done data entry job "
             "before for a compnay it was fine",
         questionnaire_response="entered data into excel sheets every day",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Poor-quality writing", experience_level="Intermediate",
         skills="python, sql",
         bio="i been coding for a while now mostly python and sql stuff for "
             "reports and things, its ok i guess, done some scripts and "
             "stuff for my last job",
         questionnaire_response="wrote a script that did some automation "
             "thing for reports i dont remember exactly what",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Poor-quality writing", experience_level="Entry",
         skills="customer service, phones",
         bio="worked a call center answerin phones and stuff for like 2 "
             "years ppl called with problems and i helpd them out mostly",
         questionnaire_response="helped alot of customers with their "
             "problems dont remember specifics",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Poor-quality writing", experience_level="Intermediate",
         skills="teaching, lesson plans",
         bio="been a teacher for a bit teach math n stuff to kids, make "
             "lesson plans and grade papers its a lot of work honestly",
         questionnaire_response="taught math class had good results i think",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Poor-quality writing", experience_level="Intermediate",
         skills="hr, recruiting",
         bio="i do hr stuff like hiring ppl and onboarding and handlin "
             "complaints n stuff its a busy job lots going on all the time",
         questionnaire_response="hired some ppl for open roles last year",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Poor-quality writing", experience_level="Entry",
         skills="video editing",
         bio="i edit videos for youtube n stuff been doin it for a bit now "
             "know premiere and after effects a little bit",
         questionnaire_response="edited some videos got decent views idk "
             "exact numbers",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Poor-quality writing", experience_level="Entry",
         skills="forklift, packing",
         bio="worked in a warehouse packin boxes and drivin forklift n "
             "stuff for like a year, its tireing work but i got used to it",
         questionnaire_response="packed alot of orders every day dont "
             "remember exact numbers",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Poor-quality writing", experience_level="Entry",
         skills="driving, deliveries",
         bio="i drive for a delivery app n stuff for like a year now, drop "
             "off packages n orders, pretty easy job honestly just drivin "
             "around all day",
         questionnaire_response="delivered alot of packages dont got exact "
             "numbers on me",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Poor-quality writing", experience_level="Entry",
         skills="cash register, stocking",
         bio="worked retail for like 2 yrs doin register n stockin shelves "
             "n stuff, dealt with customers n returns n all that",
         questionnaire_response="helped customers find stuff n did returns "
             "n stuff like that",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Poor-quality writing", experience_level="Intermediate",
         skills="construction, tools",
         bio="been doin construction for a few years now, know how to use "
             "most tools n stuff, worked on houses n small buildings n "
             "whatever",
         questionnaire_response="worked on some houses dont remember all "
             "the details",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Poor-quality writing", experience_level="Entry",
         skills="coffee, customer service",
         bio="worked at a coffee shop makin drinks n stuff for like a year, "
             "dealt with customers n cash register n cleanin up n all that",
         questionnaire_response="made alot of coffee n stuff for customers "
             "every day",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),

    # ======================================================================
    # 4. CONTRADICTORY INFORMATION  -- 12 examples
    # ======================================================================
    dict(scenario_category="Contradictory information", experience_level="Entry",
         skills="Kubernetes, Terraform, distributed systems architecture",
         bio="This is my first job application ever - I have no professional "
             "experience and haven't worked in tech before.",
         questionnaire_response="I have never built or deployed a project "
             "before.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Implausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),
    dict(scenario_category="Contradictory information", experience_level="Expert",
         skills="Python",
         bio="I have 15 years of experience as a senior Python architect "
             "leading teams of 20+ engineers at Fortune 500 companies.",
         questionnaire_response="I'm currently a first-year computer science "
             "student looking for my very first internship.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Implausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),
    dict(scenario_category="Contradictory information", experience_level="Intermediate",
         skills="Adobe Photoshop, Illustrator",
         bio="I've worked as a graphic designer for 5 years, mostly on brand "
             "identity and print materials.",
         questionnaire_response="As a backend engineer, I mostly work with "
             "PostgreSQL and Redis for caching layers.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),
    dict(scenario_category="Contradictory information", experience_level="Intermediate",
         skills="Pediatric Nursing, Patient Care",
         bio="I've been a registered nurse in a pediatric ward for six "
             "years, handling everything from routine checkups to "
             "emergency triage.",
         questionnaire_response="I'm currently finishing my final year of "
             "high school and this would be my first job of any kind.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Implausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),
    dict(scenario_category="Contradictory information", experience_level="Expert",
         skills="Financial Modeling, Investment Banking",
         bio="I spent a decade as a Vice President at a top investment bank "
             "leading M&A deals worth hundreds of millions of dollars.",
         questionnaire_response="I paint watercolor landscapes as a hobby "
             "and have never worked in an office before.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),
    dict(scenario_category="Contradictory information", experience_level="Entry",
         skills="Enterprise Sales, Salesforce",
         bio="I currently manage a $2M enterprise sales territory and close "
             "deals with Fortune 100 procurement teams on a regular basis.",
         questionnaire_response="I have never sold anything before and I'm "
             "not sure how a sales pipeline works.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),
    dict(scenario_category="Contradictory information", experience_level="Intermediate",
         skills="Curriculum Design, Classroom Management",
         bio="I've taught high school chemistry for six years and designed "
             "our department's current lab safety curriculum.",
         questionnaire_response="My most recent role was as a mechanical "
             "engineer designing turbine components for an aerospace firm.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),
    dict(scenario_category="Contradictory information", experience_level="Expert",
         skills="Architectural Design, AutoCAD, Building Codes",
         bio="I'm a licensed architect with twelve years of experience "
             "designing commercial buildings and leading project teams "
             "through permitting and construction.",
         questionnaire_response="I've never designed a building before and "
             "I'm mostly interested in learning what an architect even "
             "does.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Implausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),
    dict(scenario_category="Contradictory information", experience_level="Expert",
         skills="Cybersecurity, Penetration Testing, Network Security",
         bio="I'm a senior cybersecurity analyst with nine years of "
             "experience running penetration tests and incident response "
             "for enterprise clients.",
         questionnaire_response="I don't really use computers much outside "
             "of checking email and browsing, so I'm still learning the "
             "basics.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Implausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),
    dict(scenario_category="Contradictory information", experience_level="Expert",
         skills="Veterinary Medicine, Surgery, Animal Diagnostics",
         bio="I'm a licensed veterinarian with eleven years of experience "
             "running my own small-animal practice and performing routine "
             "surgeries.",
         questionnaire_response="I'm a sophomore in high school currently "
             "deciding what I want to study in college.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Implausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),
    dict(scenario_category="Contradictory information", experience_level="Expert",
         skills="Executive Leadership, P&L Management, Strategy",
         bio="I've served as Chief Operating Officer at a 500-person "
             "company for the past six years, overseeing all day-to-day "
             "operations and reporting directly to the board.",
         questionnaire_response="This would be my very first internship "
             "and I'm still figuring out how to write a professional "
             "email.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Implausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),
    dict(scenario_category="Contradictory information", experience_level="Intermediate",
         skills="Accounting, QuickBooks, Tax Preparation",
         bio="I've worked as a bookkeeper and tax preparer for a small "
             "accounting firm for four years, handling monthly close and "
             "individual tax returns during tax season.",
         questionnaire_response="My most recent role was as a line cook at "
             "a busy restaurant, mostly on the grill station.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Contradictory",
         expected_verdict="Flagged"),

    # ======================================================================
    # 5. IMPLAUSIBLE CLAIMS  -- 12 examples
    # ======================================================================
    dict(scenario_category="Implausible claims", experience_level="Entry",
         skills="Everything",
         bio="I am an expert in all programming languages including Python, "
             "Java, C++, Rust, Go, Haskell, and 40 others. I have personally "
             "built over 500 production applications used by a billion users "
             "combined.",
         questionnaire_response="I invented three new sorting algorithms that "
             "are faster than anything currently published.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Implausible claims", experience_level="Entry",
         skills="Machine Learning",
         bio="I graduated high school last month and have already published "
             "12 peer-reviewed papers at top AI conferences and hold 6 "
             "patents in deep learning architectures.",
         questionnaire_response="My most recent project achieved 100% "
             "accuracy on every benchmark I tested it on.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Implausible claims", experience_level="Intermediate",
         skills="Financial Advising",
         bio="I guarantee all my clients a minimum 30% annual return on "
             "their investments with absolutely zero risk of loss, every "
             "single year without exception.",
         questionnaire_response="None of my clients have ever lost money "
             "under my management, not even during market downturns.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Implausible claims", experience_level="Entry",
         skills="Digital Marketing",
         bio="Every single campaign I have ever run has gone viral, "
             "reaching over 50 million people, with a guaranteed 500% "
             "return on ad spend every time.",
         questionnaire_response="I have literally never had a campaign "
             "underperform, not even once in my career.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Implausible claims", experience_level="Intermediate",
         skills="Software Development",
         bio="I wrote an entire operating system from scratch by myself in "
             "two weeks, including the kernel, drivers, and a full GUI, "
             "with zero bugs on first release.",
         questionnaire_response="I don't use debuggers because my code is "
             "always correct the first time I write it.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Implausible claims", experience_level="Entry",
         skills="Medical Consulting",
         bio="I have personally cured several patients of chronic illnesses "
             "using a nutrition plan I developed myself, with a 100% "
             "success rate across every case I've handled.",
         questionnaire_response="My method works for literally any medical "
             "condition, no exceptions.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Implausible claims", experience_level="Entry",
         skills="Real Estate",
         bio="Every property I have ever listed sold within 24 hours at "
             "20% above asking price, in every market condition, without "
             "exception, over my entire two-year career.",
         questionnaire_response="I have a 100% close rate on every deal I "
             "have ever touched.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Implausible claims", experience_level="Entry",
         skills="Personal Training",
         bio="Every client I train loses 20 pounds of pure muscle in their "
             "first week, guaranteed, no matter their starting fitness "
             "level or medical history.",
         questionnaire_response="I have never had a client fail to see "
             "dramatic, permanent results within seven days.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Implausible claims", experience_level="Expert",
         skills="Litigation, Trial Advocacy",
         bio="In my twenty years as a trial attorney I have won every "
             "single case I've argued in court, without a single loss or "
             "settlement, across every type of litigation imaginable.",
         questionnaire_response="Judges and opposing counsel regularly tell "
             "me I'm the best litigator they've ever seen in the "
             "courtroom.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Implausible claims", experience_level="Intermediate",
         skills="Culinary Arts, Menu Design",
         bio="I single-handedly earned three Michelin stars for a "
             "restaurant I ran completely alone, cooking, plating, and "
             "serving every dish myself every single night.",
         questionnaire_response="Every dish I have ever served has "
             "received a perfect review, with zero exceptions in my "
             "career.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Implausible claims", experience_level="Entry",
         skills="Mobile App Development",
         bio="The app I built by myself over a weekend has been downloaded "
             "over one billion times and is now used by every major "
             "company in the Fortune 500.",
         questionnaire_response="I built it entirely alone with no "
             "frameworks or libraries, from scratch, in about 48 hours "
             "total.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Implausible claims", experience_level="Entry",
         skills="Photography",
         bio="I have personally photographed every major celebrity in "
             "Hollywood and every one of my photos has appeared on the "
             "cover of a major magazine, without exception.",
         questionnaire_response="Every single photoshoot I've ever done "
             "has resulted in a magazine cover, no exceptions at all.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),

    # ======================================================================
    # 6. AI-GENERATED BUT PLAUSIBLE  -- 12 examples
    # ======================================================================
    dict(scenario_category="AI-generated, plausible", experience_level="Intermediate",
         skills="React, TypeScript, GraphQL",
         bio="With over four years of hands-on experience in frontend "
             "development, I specialize in building scalable, maintainable "
             "user interfaces using React and TypeScript. I have a strong "
             "track record of collaborating with cross-functional teams to "
             "deliver polished products on schedule.",
         questionnaire_response="In my most recent role, I led the adoption "
             "of a GraphQL layer that reduced redundant API calls and "
             "improved page load performance by roughly 25 percent.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="AI-generated, plausible", experience_level="Expert",
         skills="Project Management, Agile, Stakeholder Communication",
         bio="I bring over a decade of experience managing cross-functional "
             "engineering teams in fast-paced product environments. My focus "
             "is on translating business goals into actionable sprint plans "
             "while maintaining transparent communication with stakeholders.",
         questionnaire_response="I recently coordinated a multi-team launch "
             "involving five engineering squads, delivering the release two "
             "weeks ahead of the original schedule.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="AI-generated, plausible", experience_level="Intermediate",
         skills="SQL, Python, Tableau",
         bio="I am a data analyst with three years of experience turning "
             "raw operational data into clear, actionable reporting for "
             "non-technical stakeholders. I'm comfortable owning a metric "
             "from pipeline to dashboard.",
         questionnaire_response="I built a weekly retention dashboard in "
             "Tableau that replaced four separate manual spreadsheets the "
             "team had previously relied on.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="AI-generated, plausible", experience_level="Entry",
         skills="Customer Support, Zendesk, Communication",
         bio="I'm a customer support specialist with two years of "
             "experience handling high-volume ticket queues in a B2B SaaS "
             "environment. I focus on resolving issues quickly while making "
             "sure customers feel heard.",
         questionnaire_response="I helped reduce our average response time "
             "from six hours to under two by reorganizing our ticket "
             "triage process.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="AI-generated, plausible", experience_level="Intermediate",
         skills="Content Strategy, SEO Writing, Editing",
         bio="I'm a content strategist with four years of experience "
             "writing and editing long-form content for SaaS and fintech "
             "audiences. I balance SEO requirements with genuinely useful, "
             "well-researched writing.",
         questionnaire_response="I planned and wrote a ten-part blog series "
             "that became the top organic traffic driver for the site over "
             "the following two quarters.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="AI-generated, plausible", experience_level="Intermediate",
         skills="Manual Testing, Selenium, Test Planning",
         bio="I am a QA engineer with three years of experience testing web "
             "applications, combining manual exploratory testing with "
             "automated regression suites built in Selenium.",
         questionnaire_response="I introduced a regression suite that cut "
             "our manual pre-release testing time from three days to one.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="AI-generated, plausible", experience_level="Expert",
         skills="Financial Analysis, Forecasting, Excel Modeling",
         bio="I am a financial analyst with seven years of experience "
             "building forecasting models and supporting budget planning "
             "for a mid-size manufacturing company. I focus on making "
             "financial data accessible to non-finance stakeholders.",
         questionnaire_response="I rebuilt our quarterly forecasting model, "
             "reducing the close process from two weeks to five business "
             "days.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="AI-generated, plausible", experience_level="Intermediate",
         skills="ETL Pipelines, Airflow, SQL, Python",
         bio="I am a data engineer with four years of experience building "
             "and maintaining ETL pipelines that support analytics and "
             "reporting teams. I focus on making pipelines resilient and "
             "easy to debug when something breaks at 2am.",
         questionnaire_response="I rebuilt our nightly ETL pipeline in "
             "Airflow, cutting average runtime from four hours to ninety "
             "minutes.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="AI-generated, plausible", experience_level="Intermediate",
         skills="Technical Writing, API Documentation, Markdown",
         bio="I am a technical writer with three years of experience "
             "producing developer-facing documentation for SaaS APIs. I "
             "work closely with engineering teams to keep docs accurate as "
             "products evolve.",
         questionnaire_response="I rewrote our API reference docs, which "
             "our support team says cut related support tickets "
             "noticeably.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="AI-generated, plausible", experience_level="Intermediate",
         skills="Warehouse Operations, WMS, Team Leadership",
         bio="I am a warehouse operations supervisor with five years of "
             "experience overseeing daily fulfillment operations and "
             "leading shift teams. I focus on balancing throughput targets "
             "with safe, sustainable working conditions.",
         questionnaire_response="I restructured our shift scheduling "
             "process, which reduced overtime costs while maintaining our "
             "fulfillment targets.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="AI-generated, plausible", experience_level="Intermediate",
         skills="Claims Processing, Policy Review, Compliance",
         bio="I am an insurance claims specialist with four years of "
             "experience reviewing and processing property claims. I aim "
             "to balance efficient turnaround with careful attention to "
             "policy compliance.",
         questionnaire_response="I streamlined our claims intake checklist, "
             "which reduced back-and-forth requests for missing "
             "documentation.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="AI-generated, plausible", experience_level="Intermediate",
         skills="User Research, Usability Testing, Survey Design",
         bio="I am a UX researcher with three years of experience running "
             "qualitative and quantitative studies for consumer mobile "
             "products. I work to make research findings actionable for "
             "product and design teams.",
         questionnaire_response="I ran a usability study on our checkout "
             "flow that identified a confusing step, which the design team "
             "used to simplify the process.",
         source="AI", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),

    # ======================================================================
    # 7. AI-GENERATED AND SUSPICIOUS  -- 12 examples
    # ======================================================================
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="Full-Stack Development, Cloud Architecture, Machine Learning, DevOps",
         bio="As a highly motivated and results-driven professional, I "
             "possess an extensive and diverse skill set spanning full-stack "
             "development, cloud architecture, machine learning, and DevOps "
             "practices, enabling me to seamlessly deliver end-to-end "
             "solutions that consistently exceed stakeholder expectations.",
         questionnaire_response="Leveraging synergistic best practices, I "
             "have consistently delivered cutting-edge, scalable solutions "
             "across a wide array of complex, mission-critical projects.",
         source="AI", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="Everything relevant",
         bio="I am a dedicated and passionate individual with a proven track "
             "record of excellence across numerous domains, consistently "
             "demonstrating an unwavering commitment to delivering "
             "exceptional results in any environment I am placed in.",
         questionnaire_response="I have successfully completed numerous "
             "high-impact projects that showcase my exceptional abilities "
             "and unmatched dedication to quality.",
         source="AI", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="Marketing, Branding, Growth",
         bio="As a dynamic and forward-thinking marketing professional, I "
             "excel at leveraging innovative strategies to drive impactful, "
             "data-driven growth across multiple channels, consistently "
             "delivering unparalleled results that exceed every KPI target.",
         questionnaire_response="I spearheaded a game-changing initiative "
             "that revolutionized our brand's market positioning and "
             "unlocked unprecedented levels of engagement.",
         source="AI", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="Sales, Negotiation, Client Relations",
         bio="As a results-oriented sales professional with an unwavering "
             "commitment to excellence, I consistently exceed targets by "
             "leveraging a client-centric approach that drives sustainable, "
             "long-term revenue growth across every account I manage.",
         questionnaire_response="I have consistently closed every deal I "
             "have pursued, exceeding quota by significant margins each and "
             "every quarter without fail.",
         source="AI", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="Human Resources, Talent Acquisition",
         bio="As a strategic and people-first HR professional, I bring a "
             "wealth of expertise in talent acquisition, employee "
             "engagement, and organizational development, consistently "
             "fostering a culture of excellence and driving transformative "
             "outcomes across every initiative I lead.",
         questionnaire_response="I have single-handedly transformed company "
             "culture at every organization I've touched, achieving "
             "unprecedented levels of employee satisfaction.",
         source="AI", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="Operations Management, Process Improvement",
         bio="As a dedicated operations professional, I leverage a "
             "comprehensive, synergistic approach to process optimization, "
             "consistently delivering transformative efficiencies that "
             "unlock exponential value across every facet of the "
             "organization I serve.",
         questionnaire_response="I have optimized every process I have "
             "ever touched, achieving perfect efficiency across all "
             "operational workflows without exception.",
         source="AI", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="Teaching, Curriculum Development",
         bio="As a passionate and student-centered educator, I am "
             "committed to fostering transformative learning experiences "
             "that empower every student to achieve unparalleled academic "
             "excellence through innovative, research-backed pedagogical "
             "strategies.",
         questionnaire_response="Every single one of my students has "
             "achieved top marks under my instruction, without exception, "
             "across every class I have ever taught.",
         source="AI", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="Legal Consulting, Contract Review",
         bio="As a meticulous and detail-oriented legal professional, I "
             "leverage a comprehensive understanding of regulatory "
             "frameworks to consistently deliver airtight, risk-mitigating "
             "solutions that empower organizations to navigate complex "
             "legal landscapes with total confidence.",
         questionnaire_response="I have reviewed and finalized every "
             "contract flawlessly, with zero errors or disputes across my "
             "entire career.",
         source="AI", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="Program Coordination, Community Outreach",
         bio="As a passionate and mission-driven program coordinator, I "
             "leverage a holistic, community-centered approach to drive "
             "transformative social impact, consistently exceeding "
             "engagement targets and fostering unparalleled stakeholder "
             "alignment across every initiative.",
         questionnaire_response="Every program I have coordinated has "
             "achieved perfect community engagement, exceeding all targets "
             "without exception.",
         source="AI", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="Photography, Visual Storytelling",
         bio="As a visionary and detail-obsessed visual storyteller, I "
             "leverage a unique creative lens to consistently deliver "
             "breathtaking, awe-inspiring imagery that captures the "
             "essence of every moment with unparalleled artistic "
             "precision.",
         questionnaire_response="Every single photograph I have ever taken "
             "has been praised as a masterpiece by everyone who has seen "
             "it.",
         source="AI", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="Fitness Coaching, Nutrition",
         bio="As a transformative and results-obsessed fitness coach, I "
             "leverage a holistic, science-backed methodology to "
             "consistently deliver unparalleled physical transformations "
             "that empower every client to achieve their ultimate fitness "
             "potential.",
         questionnaire_response="Every client I have ever coached has "
             "achieved dramatic, life-changing results within their first "
             "week, without exception.",
         source="AI", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="AI-generated, suspicious", experience_level="Entry",
         skills="IT Support, Helpdesk, Troubleshooting",
         bio="As a highly skilled and proactive IT support professional, I "
             "leverage a comprehensive technical toolkit to consistently "
             "deliver seamless, frictionless resolutions that empower "
             "end-users to achieve uninterrupted productivity at all "
             "times.",
         questionnaire_response="I have resolved every single ticket on "
             "the first attempt with zero escalations across my entire "
             "career.",
         source="AI", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),

    # ======================================================================
    # 8. HUMAN-WRITTEN BUT SUSPICIOUS  -- 12 examples
    # ======================================================================
    dict(scenario_category="Human-written, suspicious", experience_level="Expert",
         skills="Everything you need honestly",
         bio="look ive done it all, every framework, every language, trust "
             "me im the best hire youll ever make no cap, been coding since "
             "before i could walk basically",
         questionnaire_response="cant think of a specific project rn but "
             "trust me ive done way bigger stuff than youd expect",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Human-written, suspicious", experience_level="Intermediate",
         skills="Sales",
         bio="I closed over 10 million dollars in deals last quarter working "
             "solo with no team and no CRM, all cold calls, best salesperson "
             "this industry has ever seen honestly.",
         questionnaire_response="Every single deal I have ever pitched has "
             "closed, 100% success rate, no exceptions.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Human-written, suspicious", experience_level="Intermediate",
         skills="Coding, basically everything",
         bio="honestly im just built different when it comes to coding, "
             "never had a bug in production ever, other devs on my old team "
             "used to call me the goat fr",
         questionnaire_response="cant name a specific project but i built "
             "way more impressive stuff than most senior devs tbh",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Human-written, suspicious", experience_level="Intermediate",
         skills="social media, marketing",
         bio="everything i post goes viral no joke, i have like a golden "
             "touch for content, every brand i worked with blew up "
             "immediately after i started",
         questionnaire_response="cant remember exact numbers but trust me "
             "it was a lot of views, like a crazy amount honestly",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Human-written, suspicious", experience_level="Expert",
         skills="Investing, Trading",
         bio="ive never lost money on a single trade in my whole career, "
             "not once, i basically have a sixth sense for the market that "
             "nobody else has",
         questionnaire_response="every prediction ive made has come true "
             "so far, no exceptions, ask anyone who knows me",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Human-written, suspicious", experience_level="Intermediate",
         skills="Teaching",
         bio="im honestly the best teacher this school has ever had, every "
             "single kid in my class gets an A, parents literally beg to "
             "get their kids into my class every year",
         questionnaire_response="cant think of a specific lesson but "
             "everything i teach just works perfectly every time",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Human-written, suspicious", experience_level="Intermediate",
         skills="Customer Support",
         bio="ive literally never had a single customer complaint in three "
             "years, not one, every ticket i touch ends with a five star "
             "review no matter what",
         questionnaire_response="cant name a specific case but trust me "
             "everyone loves working with me, no exceptions ever",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Human-written, suspicious", experience_level="Intermediate",
         skills="Auto Repair, Diagnostics",
         bio="ive fixed every car thats ever come into my shop first try, "
             "no come backs ever, other mechanics dont even come close to "
             "how good i am honestly",
         questionnaire_response="cant think of a specific repair but trust "
             "me ive never gotten one wrong in my whole career",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Human-written, suspicious", experience_level="Intermediate",
         skills="Photography",
         bio="literally every photo ive ever taken has been perfect first "
             "try, no edits needed ever, clients always say im better than "
             "photographers whove been doin it for 20 years",
         questionnaire_response="cant name a specific shoot but trust me "
             "theyre all amazing, every single one honestly",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Human-written, suspicious", experience_level="Expert",
         skills="Law, Litigation",
         bio="never lost a case in my whole career not even one, judges "
             "literally know my name and juries always side with me no "
             "matter what the case is about honestly",
         questionnaire_response="cant think of a specific case but trust "
             "me i win every single time without fail",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Human-written, suspicious", experience_level="Intermediate",
         skills="Personal Training",
         bio="everyone i train gets a six pack in like a week no matter "
             "what they looked like before, its basically magic honestly "
             "im just built different as a trainer",
         questionnaire_response="cant name a specific client but trust me "
             "the results are always insane no exceptions",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),
    dict(scenario_category="Human-written, suspicious", experience_level="Intermediate",
         skills="Cooking, Restaurant Management",
         bio="honestly im the best chef this city has ever seen, every "
             "dish i make gets perfect reviews, restaurants beg me to come "
             "work for them all the time no cap",
         questionnaire_response="cant think of a specific dish but trust "
             "me everything i cook is basically flawless every time",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Implausible", consistency_label="Consistent",
         expected_verdict="Flagged"),

    # ======================================================================
    # 9. MIXED HUMAN/AI-EDITED TEXT  -- 12 examples
    # ======================================================================
    dict(scenario_category="Mixed human/AI-edited", experience_level="Intermediate",
         skills="Python, SQL, Tableau",
         bio="I've been working as a data analyst for about three years now, "
             "mostly building dashboards and running ad-hoc queries for the "
             "marketing team. Leveraging a robust analytical toolkit, I "
             "consistently deliver actionable insights that drive strategic "
             "decision-making across the organization.",
         questionnaire_response="Built a Tableau dashboard that the "
             "marketing team still uses weekly to track campaign ROI.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Mixed human/AI-edited", experience_level="Entry",
         skills="Customer Support, Zendesk",
         bio="I worked at a call center for a year answering customer "
             "questions about billing. As a highly motivated professional, "
             "I am committed to delivering world-class customer experiences "
             "at every touchpoint.",
         questionnaire_response="Handled about 40-60 support tickets a day, "
             "mostly billing disputes and account access issues.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Mixed human/AI-edited", experience_level="Intermediate",
         skills="Figma, UI Design",
         bio="I've designed mobile app interfaces for two years at a small "
             "startup. Passionate about crafting intuitive, user-centric "
             "experiences that seamlessly blend aesthetics with "
             "functionality to drive meaningful engagement.",
         questionnaire_response="Redesigned our app's checkout flow, which "
             "our team believes helped reduce cart abandonment, though we "
             "never formally measured it.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Mixed human/AI-edited", experience_level="Intermediate",
         skills="React, JavaScript",
         bio="I've built a handful of small web apps for local businesses "
             "as freelance work over the past two years. Committed to "
             "writing clean, maintainable code that empowers businesses to "
             "achieve their digital transformation goals.",
         questionnaire_response="Built a booking site for a local hair "
             "salon that they still use to take appointments.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Mixed human/AI-edited", experience_level="Intermediate",
         skills="Recruiting, Onboarding",
         bio="I've worked in recruiting for three years at a small agency, "
             "mostly filling admin and entry-level roles. Dedicated to "
             "identifying top talent and fostering a seamless, "
             "candidate-centric hiring experience from first contact to "
             "offer.",
         questionnaire_response="Filled about 15 roles last year, mostly "
             "for local retail and admin positions.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Mixed human/AI-edited", experience_level="Entry",
         skills="Copywriting, Blogging",
         bio="I've written blog posts for a few small clients on Upwork "
             "over the last year. Skilled at crafting compelling, "
             "SEO-optimized content that resonates with target audiences "
             "and drives measurable engagement.",
         questionnaire_response="Wrote about 20 blog posts for a small "
             "gardening supply store's website.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Mixed human/AI-edited", experience_level="Intermediate",
         skills="Sales, Cold Outreach",
         bio="I've done outbound sales for a small SaaS company for about "
             "two years, mostly cold email and LinkedIn outreach. "
             "Passionate about building genuine relationships that drive "
             "sustainable pipeline growth and exceed revenue targets.",
         questionnaire_response="Booked around 5-8 qualified meetings a "
             "week through cold outreach, converting maybe one in six to a "
             "paying customer.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Mixed human/AI-edited", experience_level="Intermediate",
         skills="Warehouse Coordination, Inventory Systems",
         bio="I've coordinated inventory for a mid-size warehouse for two "
             "years. Committed to leveraging best-in-class logistics "
             "practices to drive operational excellence and seamless "
             "supply chain efficiency.",
         questionnaire_response="Reorganized our inventory labeling system, "
             "which the team believes cut picking errors, though we never "
             "tracked exact numbers.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Mixed human/AI-edited", experience_level="Intermediate",
         skills="Legal Assistance, Filing, Scheduling",
         bio="I've worked as a legal assistant at a small firm for two "
             "years handling filing and scheduling. Dedicated to providing "
             "meticulous, detail-oriented support that ensures seamless "
             "case management from intake to resolution.",
         questionnaire_response="Organized case files for around 30 active "
             "matters, which the attorneys said made things easier to "
             "find.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Mixed human/AI-edited", experience_level="Entry",
         skills="IT Support, Ticketing Systems",
         bio="I did IT support for a small office for about a year, mostly "
             "resetting passwords and fixing printer issues. Dedicated to "
             "delivering exceptional technical support that empowers users "
             "to work without interruption.",
         questionnaire_response="Handled about 10-15 tickets a day, mostly "
             "account access and basic hardware troubleshooting.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Mixed human/AI-edited", experience_level="Intermediate",
         skills="Claims Review, Customer Communication",
         bio="I've processed insurance claims for two years at a regional "
             "office. Committed to delivering thorough, client-centric "
             "claims review that balances efficiency with careful attention "
             "to detail.",
         questionnaire_response="Processed roughly 15-20 claims a week, "
             "mostly auto and home property claims.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Mixed human/AI-edited", experience_level="Entry",
         skills="User Interviews, Surveys",
         bio="I helped run a few user interviews for a class project last "
             "year. Passionate about uncovering deep user insights that "
             "drive meaningful, human-centered product decisions.",
         questionnaire_response="Interviewed about 8 users for a mock app "
             "redesign project as part of my coursework.",
         source="Mixed", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),

    # ======================================================================
    # 10. EDGE CASES  -- 12 examples
    # ======================================================================
    dict(scenario_category="Edge case - very short but genuine", experience_level="Entry",
         skills="Python",
         bio="Recent CS grad. Built a few small Python scripts and a Flask "
             "API for a class project. Looking for my first role.",
         questionnaire_response="Built a to-do list API with Flask and "
             "SQLite for my final year project.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Edge case - unusually long bio", experience_level="Intermediate",
         skills="C++, Embedded Systems",
         bio="I started programming when I was thirteen, teaching myself C "
             "from library books because my school didn't offer computer "
             "science classes. In university I focused on embedded systems, "
             "working on a robotics team that competed nationally for three "
             "years running. After graduating I joined a small hardware "
             "startup where I wrote firmware for battery management systems, "
             "which taught me a lot about the constraints of memory-limited "
             "environments. Two years ago I moved to a larger company "
             "working on industrial IoT sensors, where I currently maintain "
             "a C++ codebase running on several thousand deployed devices.",
         questionnaire_response="Rewrote our sensor firmware's power "
             "management logic, extending average battery life from 8 to 14 "
             "months across our device fleet.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Edge case - minimal skills, strong bio", experience_level="Entry",
         skills="Curiosity",
         bio="I don't have formal technical skills listed because I'm "
             "coming from a non-technical background - five years in "
             "high-school teaching - but I've spent the last eight months "
             "self-studying web development every evening and built two "
             "small projects I'm proud of.",
         questionnaire_response="Built a simple grade-tracking web app for "
             "my own classroom using HTML, CSS, and vanilla JS.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Edge case - non-English mixed in", experience_level="Intermediate",
         skills="Traduction, Content Writing, SEO",
         bio="Je suis redactrice freelance depuis trois ans, specialisee "
             "dans le contenu SEO en francais et en anglais. I also write "
             "blog content for English-speaking clients in the SaaS space.",
         questionnaire_response="Wrote a 12-part blog series for a SaaS "
             "client that doubled their organic traffic over six months.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Edge case - numeric/keyword-only skills", experience_level="Entry",
         skills="3, 5, JS, ok",
         bio="did some coding stuff in school, made a website once for a "
             "class thing, not sure what else to say here honestly",
         questionnaire_response="made a website for a school project, it "
             "had a homepage and a contact form",
         source="Human", completeness_label="Yes", text_quality_label="Poor",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Edge case - all caps formatting", experience_level="Intermediate",
         skills="PROJECT MANAGEMENT, AGILE, SCRUM",
         bio="I HAVE FIVE YEARS OF EXPERIENCE MANAGING SOFTWARE PROJECTS "
             "USING AGILE METHODOLOGY. I HAVE LED MULTIPLE SUCCESSFUL "
             "PRODUCT LAUNCHES AND ENJOY COORDINATING CROSS-FUNCTIONAL "
             "TEAMS.",
         questionnaire_response="LED A TEAM OF SIX ENGINEERS THROUGH A "
             "MAJOR PLATFORM MIGRATION COMPLETED ON SCHEDULE.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Edge case - career changer", experience_level="Entry",
         skills="SQL, Excel, basic Python",
         bio="I spent nine years as a high school math teacher before "
             "deciding to move into data analysis. I completed a part-time "
             "data analytics certificate over the last year while still "
             "teaching, and built two small analysis projects using public "
             "datasets.",
         questionnaire_response="Analyzed five years of my school's "
             "attendance data in Python to identify seasonal absence "
             "patterns, which the administration used to adjust scheduling.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Verified"),
    dict(scenario_category="Edge case - emoji-heavy formatting", experience_level="Entry",
         skills="Social Media, Canva, Instagram",
         bio="hii!! im a social media person who LOVES creating content "
             "for brands, ive worked with a few small local shops doing "
             "their instagram and it was so fun, always down to learn "
             "more and grow!!",
         questionnaire_response="made instagram posts for a local bakery "
             "that got a decent amount of engagement, they were happy "
             "with it!",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Edge case - resume-paste bullet format", experience_level="Intermediate",
         skills="Project Coordination, MS Office, Scheduling",
         bio="- Coordinated cross-departmental projects for 3 years\n"
             "- Managed vendor relationships and procurement\n"
             "- Built weekly status reports for leadership\n"
             "- Trained 2 new coordinators on internal processes",
         questionnaire_response="- Led scheduling for a 6-month office "
             "relocation project\n- Delivered on time and under budget",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Edge case - overqualified for entry role", experience_level="Entry",
         skills="Strategic Planning, Team Leadership, P&L Management",
         bio="After fifteen years as a regional operations director, I "
             "recently relocated and am deliberately looking for an "
             "entry-level role to rebuild local experience and take some "
             "career pressure off for a while.",
         questionnaire_response="Managed operations across 12 retail "
             "locations in my previous role, though I'm applying here for "
             "something lower-key.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Edge case - single sentence, genuine", experience_level="Entry",
         skills="Customer Service",
         bio="I worked front desk at a hotel for a year and I'm looking "
             "for something similar with more responsibility.",
         questionnaire_response="Checked guests in and out and handled "
             "basic complaints about room issues.",
         source="Human", completeness_label="Yes", text_quality_label="Fair",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
    dict(scenario_category="Edge case - skills/role mismatch but plausible", experience_level="Entry",
         skills="Music Production, Audio Engineering",
         bio="I've spent the last three years as a freelance audio "
             "engineer for local bands, but I'm looking to transition into "
             "customer support roles since steady freelance income has "
             "been unpredictable.",
         questionnaire_response="Mixed and mastered an EP for a local band "
             "that got some regional radio play, but I'm ready for a "
             "career change.",
         source="Human", completeness_label="Yes", text_quality_label="Good",
         plausibility_label="Plausible", consistency_label="Consistent",
         expected_verdict="Needs Improvement"),
]


def main():
    rows = []
    for i, ex in enumerate(EXAMPLES, start=1):
        row = {"submission_id": f"S{i:03d}"}
        row.update(ex)
        rows.append(row)

    random.shuffle(rows)  # avoid category-ordered bias in downstream splits

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT_PATH}")

    from collections import Counter
    cat_counts = Counter(r["scenario_category"] for r in rows)
    verdict_counts = Counter(r["expected_verdict"] for r in rows)
    print("\nRows per category:")
    for cat, n in sorted(cat_counts.items()):
        print(f"  {n:>3}  {cat}")
    print("\nRows per expected verdict:")
    for v, n in sorted(verdict_counts.items()):
        print(f"  {n:>3}  {v}")


if __name__ == "__main__":
    main()
