# Daily Onboarding Notes: UX vNext & Risk Strategy
**Document Creation Date:** February 18, 2026
**Theme:** Escalated Journeys, Underwriting Alignment, and Product Quotability

---

## 1. Executive Summary
Today’s session focused on "Escalated Journeys" and the tension between fraud prevention and conversion. A key conflict has emerged with the underwriter **First**, who wants to restrict users over 23 due to fraud concerns. The internal counter-proposal is to use **Emailage** (identity data) as a more surgical tool for blocking fraud rather than blunt age-based stops. The goal is to move toward a "Single Product Journey" while improving **Quotability**—the ratio of users who actually receive a price versus a decline.

---

## 2. Today's Key Notes

### **Escalated Journeys & Fraud Prevention**
* **The "First" Conflict:** The underwriter (First) wants to shut down accounts for those **over 23** due to high fraud prevalence (approx. 100 accounts impacted).
* **Counter-Proposal:** We are proposing a move to block only those with an **Emailage under 5 days** (a high indicator of burner emails used for fraud). This would only impact 16 accounts, significantly preserving conversion compared to the age-based block.
* **UX Strategy:** Alice is researching a "better version" of this flow to handle risk-based friction without killing the user experience.

### **Underwriting & Architecture**
* **Data Origins:** Need to understand the end-to-end architecture of where the **price is determined** and where we keep declining people.
* **Historical Context:** The question set was reduced from **20 questions to 12**. I need to understand what specific friction was removed.
* **Key Concept: Quotability:** Defined as the number of users who request a quote and successfully receive one. Improving this is a direct lever for conversion.

---

## 3. Questions Asked & Answers Given

**Q: What are escalated journeys?**
**A:** [To be confirmed/Follow up with Alice] Generally refers to journeys where high-risk signals trigger additional verification or specific underwriter-mandated paths.

**Q: Why do we keep declining people?**
**A:** "Risk Declined" occurs when a user does not meet the specific risk profile/appetite of the current underwriting panel.

**Q: What was the reference to 20 questions vs 12?**
**A:** [Follow up with Christine/Alice] Likely refers to the reduction in the "Risk Details" form to speed up conversion.

---

## 4. Updates to "The Two-Week" To-Do List
- [ ] **Stakeholder Intro:** Connect with **Jake** (Underwriting) to discuss loss ratios.
- [ ] **Technical Deep Dive:** Meet with **Joel** (Radar Dev) to map out how/where Radar determines the final price.
- [ ] **Documentation Request:** Ask **Alice** to share previous conversations with **Christine** (Senior Technical Underwriter).
- [ ] **Strategy Research:** Review Neil’s "Single Product Journey" ideas.
- [ ] **Underwriting Intro:** Sync with **Marc Pell**.

---

## 5. Vocabulary / Jargon Observed
| Term | Definition |
| :--- | :--- |
| **Escalated Journey** | A high-risk user path requiring extra validation. |
| **Emailage** | A 3rd party tool (LexisNexis) that scores the risk of an email address based on its "age" and history. |
| **Quotability** | The % of users who reach the quote screen and are actually offered a price (vs. a decline). |
| **Radar** | The 3rd party decision engine (Willis Towers Watson) where our pricing models live. |
| **Loss Ratio** | The ratio of claims paid out vs. premiums earned (Critical for underwriter happiness). |

---