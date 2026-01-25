---
title: Privacy Policy
permalink: /legal/privacy/
---

# Privacy Policy

**BrainDock Focus Tracking Application**

Last Updated: January 2026

---

## 1. Introduction

BrainDock ("we", "us", "our") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our focus tracking application ("the Application").

This policy is designed to comply with the Australian Privacy Principles (APPs) under the Privacy Act 1988 (Cth), as well as provide transparency for users in other jurisdictions including the European Union (GDPR) and United Kingdom (UK GDPR).

**Please read this Privacy Policy carefully.** By using the Application, you consent to the practices described in this policy.

---

## 2. About Us

BrainDock is a focus tracking application that helps users monitor their study and work sessions using camera-based presence detection.

**Contact Information:**

- Email: morayyajain@gmail.com
- Website: thebraindock.com
- Address: 108-128 Leicester Street, Carlton, VIC-3053

---

## 3. Information We Collect

We collect different types of information to provide and improve our service.

### 3.1 Camera Frame Data (Processed, Not Stored)

**What we capture:**
- Visual frames from your device's camera during active sessions

**What we analyse:**
- Whether a person is present at the desk
- Whether the person appears to be engaged with distraction devices (phones, tablets, game controllers)
- General posture/presence indicators (at desk vs. away)

**What we do NOT analyse or collect:**
- Your identity or facial features for recognition purposes
- Biometric templates or biometric identifiers
- Audio from your microphone
- Keystrokes or typing content

**Processing:**
- Frames are captured approximately once per second during active sessions only
- Frames are transmitted to our AI processing providers (OpenAI or Google Gemini) for analysis
- Frames are NOT stored locally on your device
- Frames are NOT stored on our servers

### 3.2 Screen Monitoring Data (Processed Locally)

**What we monitor:**
- Active window titles (e.g., "YouTube - Google Chrome")
- Browser URLs when detectable
- Active application names

**How it works:**
- Window titles and URLs are compared against your blocklist of distraction apps/websites
- This processing happens **locally on your device**
- Window titles and URLs are NOT sent to third-party services (unless AI Screenshot Analysis is enabled)

**What we do NOT monitor:**
- Content within windows or applications
- Text you type or read
- Files you open or create

### 3.3 Optional Screenshot Data (User-Controlled)

**This feature is disabled by default.** You must explicitly enable it in Application settings.

**When enabled:**
- The Application captures screenshots of your screen
- Screenshots are transmitted to our AI providers (OpenAI or Google Gemini) for analysis
- AI analyses the screenshot to detect distraction content
- Screenshots are processed in real-time and **NOT stored** on your device or our servers

**What the AI analyses:**
- Whether distraction apps/websites are visible
- General screen content category (work, entertainment, social media, etc.)

**What the AI does NOT extract:**
- Text content or readable information from screenshots
- Personal data visible on screen
- File names, passwords, or sensitive information

**Important warnings:**
- Screenshots may capture sensitive information visible on your screen
- Ensure no confidential information is visible when this feature is enabled
- You can disable this feature at any time

### 3.5 Session Log Data (Stored Locally)

The following data is generated and stored locally on your device:

| Data Type | Description | Storage Location |
|-----------|-------------|------------------|
| Session timestamps | Start and end times of focus sessions | Your device |
| Event logs | Timestamps of state changes (present, away, distraction detected) | Your device |
| Focus statistics | Calculated metrics (focus time, distraction count, etc.) | Your device |
| Session reports | Generated PDF summaries | Your device (Downloads folder) |

### 3.6 Licence and Payment Data

When you purchase the Application:

| Data Type | Collected By | Purpose |
|-----------|--------------|---------|
| Email address | Stripe (payment processor) | Payment confirmation, licence delivery |
| Payment details | Stripe | Process payment |
| Licence key | Stored locally | Validate your licence |
| Terms acceptance | Stripe | Record of consent |

We do not directly collect or store your payment card details.

### 3.7 Technical and Diagnostic Data

We may collect minimal technical data for troubleshooting:

- Error logs (may include timestamps, error messages)
- Application version
- Operating system type

**Note:** We design our logging to avoid capturing personal information. However, error logs may inadvertently contain personal data in some circumstances.

---

## 4. Explicit Statement: No Biometric Data Collection

**We explicitly confirm that BrainDock does NOT collect biometric information.**

Specifically, we do NOT:

- Perform facial recognition or facial identification
- Create facial geometry maps or templates
- Store biometric identifiers or biometric templates
- Use biometric information for automated biometric verification or identification
- Match or verify user identity using biological characteristics
- Create profiles that could uniquely identify you

Our AI processing analyses only:
- General presence (is a person visible?)
- Position (is the person at the desk or away?)
- Object detection (is a phone/tablet/controller being actively used?)

This is fundamentally different from biometric processing. We process the content of frames to detect objects and presence—we do not extract or store any biometric characteristics.

---

## 5. How We Use Your Information

We use collected information for the following purposes:

| Purpose | Legal Basis (GDPR) | APP Reference |
|---------|-------------------|---------------|
| Provide focus tracking functionality | Contract performance / Consent | APP 3, 6 |
| Generate session reports | Contract performance | APP 6 |
| Process payments | Contract performance | APP 3, 6 |
| Validate licences | Legitimate interest | APP 6 |
| Improve the Application | Legitimate interest | APP 6 |
| Respond to support requests | Contract performance | APP 6 |
| Comply with legal obligations | Legal obligation | APP 6 |

---

## 6. Disclosure to Third Parties

### 6.1 AI Processing Providers

We use third-party AI services for image analysis. **Only one provider is used at a time** during any given session, but we may switch between providers. Our current providers are:

---

#### 6.1.1 OpenAI

**What is disclosed:** Camera frames during active sessions

**Why:** To perform AI-based presence and object detection

**Location:** United States

**Their data practices:**
- OpenAI's API Data Usage Policy states they may retain API data for up to 30 days for safety and abuse monitoring
- OpenAI does not use API data to train their models (as of their current policy)
- OpenAI Privacy Policy: https://openai.com/privacy
- OpenAI API Data Usage: https://openai.com/policies/api-data-usage-policies

---

#### 6.1.2 Google (Gemini)

**What is disclosed:** Camera frames during active sessions

**Why:** To perform AI-based presence and object detection

**Location:** United States

**Their data practices:**
- Google's Gemini API may retain data for safety monitoring and abuse prevention
- Google does not use Gemini API data to train their models (per their current API terms)
- Google Privacy Policy: https://policies.google.com/privacy
- Google Cloud Data Processing Terms: https://cloud.google.com/terms/data-processing-terms
- Gemini API Terms: https://ai.google.dev/gemini-api/terms

---

**Our safeguards (apply to all providers):**
- We use API-only services (not consumer products)
- We send only the minimum data required for analysis
- We use optimised settings to reduce data transmission where available
- We do not send identifying metadata with frames

### 6.2 Payment Processor (Stripe)

**What is disclosed:** Payment and contact information you provide at checkout

**Why:** To process your payment and deliver your licence

**Location:** United States (with global operations)

**Their data practices:** https://stripe.com/privacy

### 6.3 Other Disclosures

We may disclose your information:

- **Legal Requirements:** If required by law, court order, or government request
- **Protection of Rights:** To protect our rights, privacy, safety, or property
- **Business Transfer:** In connection with a merger, acquisition, or sale of assets (with notice to you)

We do NOT:
- Sell your personal information
- Share data for third-party marketing
- Trade in personal information

---

## 7. Cross-Border Data Transfers (APP 8)

Your camera frame data is transferred to the United States for processing by our AI providers (OpenAI and/or Google Gemini).

### 7.1 Why We Transfer Data Overseas

We use cloud-based AI vision APIs (OpenAI Vision and Google Gemini) because they provide the most accurate and privacy-preserving method for presence detection without requiring on-device facial recognition or biometric processing.

### 7.2 Protections for Overseas Transfers

We take the following steps to protect your data:

1. **Contractual Protections:** Both OpenAI and Google are bound by their published data usage policies and enterprise terms
2. **Data Minimisation:** We send only camera frames (and screenshots if enabled), not identifying metadata
3. **No Permanent Storage:** Frames and screenshots are processed in real-time and not permanently stored by us
4. **Reputable Providers:** Both OpenAI and Google maintain SOC 2 compliance and enterprise security standards

### 7.3 Your Consent

By using the Application, you consent to this cross-border transfer. If you do not consent, please do not use the Application.

### 7.4 EU/UK Users

For users in the European Union or United Kingdom, transfers to the US are conducted in accordance with applicable data transfer mechanisms under GDPR/UK GDPR.

---

## 8. Data Retention Schedule

We maintain the following retention practices:

| Data Type | Retention Period | Deletion Method |
|-----------|------------------|-----------------|
| Camera frames | Not retained (processed in real-time only) | Not applicable |
| Screenshots (if enabled) | Not retained (processed in real-time only) | Not applicable |
| Screen monitoring data | Not retained (processed locally in real-time) | Not applicable |
| Session logs (local) | Until you delete them | User-controlled deletion |
| PDF reports (local) | Until you delete them | User-controlled deletion |
| Error logs | 30 days maximum | Automatic deletion |
| Licence data | Duration of licence validity | Upon licence revocation |
| Payment records (Stripe) | Per Stripe's retention policy | Contact Stripe |
| OpenAI processing | Up to 30 days per OpenAI policy | Automatic per OpenAI |
| Google Gemini processing | Per Google's retention policy | Automatic per Google |

### 8.1 Your Control Over Local Data

All session data and reports are stored locally on your device. You can delete this data at any time by:

1. Deleting files from the Application's data directory
2. Uninstalling the Application
3. Using your operating system's file management tools

### 8.2 Data We Cannot Delete

Once frames are transmitted to our AI providers (OpenAI or Google Gemini), their retention is governed by those providers' respective policies. We cannot delete this data on your behalf. Both providers may retain data for up to 30 days for safety and abuse monitoring purposes.

---

## 9. Data Security (APP 11)

We implement reasonable security measures to protect your information:

### 9.1 Technical Measures

- **Encryption in Transit:** All data transmitted to third parties uses TLS/HTTPS encryption
- **Local Storage:** Session data is stored in standard file formats on your device, protected by your device's security
- **No Central Database:** We do not maintain a central database of user session data
- **API Security:** We use secure API authentication with our service providers

### 9.2 Organisational Measures

- Access to systems is limited to authorised personnel
- We follow secure development practices
- We regularly review and update security measures

### 9.3 Your Responsibilities

You are responsible for:
- Securing your device with appropriate passwords/biometrics
- Keeping your operating system and the Application updated
- Not sharing your licence key with others
- Protecting any exported reports containing session data

---

## 10. Data Breach Response

### 10.1 Our Commitment

In the event of a data breach that is likely to result in serious harm to you, we will:

1. **Assess** the breach within 30 days to determine severity
2. **Notify** affected individuals as soon as practicable
3. **Report** to the Office of the Australian Information Commissioner (OAIC) if required under the Notifiable Data Breaches scheme
4. **Take steps** to contain the breach and prevent recurrence

### 10.2 What We Will Tell You

If we need to notify you of a breach, we will provide:
- A description of the breach
- The types of information involved
- Recommendations for protective steps you can take
- Our contact information for further questions

### 10.3 Limitations

Because we do not store camera frames and session data is stored locally on your device, the most likely breach scenarios involve:
- Compromise of our AI provider's systems (governed by their incident response)
- Compromise of payment processor systems (governed by Stripe's incident response)
- Unauthorised access to your local device (your responsibility to report to relevant authorities)

---

## 11. Your Privacy Rights

### 11.1 Australian Users (APP 12, 13)

Under the Australian Privacy Principles, you have the right to:

- **Access:** Request access to personal information we hold about you
- **Correction:** Request correction of inaccurate information
- **Complaint:** Lodge a complaint if you believe we have breached the APPs

To exercise these rights, contact us using the details in Section 2.

**Note:** Because most data is stored locally on your device, you already have direct access to and control over this information.

### 11.2 EU/UK Users (GDPR Rights)

If you are in the EU or UK, you have additional rights including:

- Right to erasure ("right to be forgotten")
- Right to restrict processing
- Right to data portability
- Right to object to processing
- Rights related to automated decision-making

### 11.3 How to Make a Request

Contact us at morayyajain@gmail.com with:
- Your name and contact details
- A description of what you are requesting
- Any information to help us locate your data

We will respond within 30 days (or sooner if required by applicable law).

### 11.4 Complaints

If you are not satisfied with our response, you may lodge a complaint with:

**Australia:**
Office of the Australian Information Commissioner (OAIC)
- Website: www.oaic.gov.au
- Phone: 1300 363 992

**EU:**
Your local Data Protection Authority

**UK:**
Information Commissioner's Office (ICO)
- Website: www.ico.org.uk

---

## 12. Third-Party Capture Warning

**IMPORTANT:** Your camera may capture other people in your environment.

### 12.1 Your Obligations

If other individuals may appear in your camera's view (housemates, family members, colleagues, visitors, people on video calls), **you are responsible for:**

- Informing them that camera capture is occurring
- Obtaining their consent where required by law
- Positioning your camera to minimise third-party capture
- Not using the Application if you cannot obtain appropriate consent

### 12.2 Our Limitations

We cannot:
- Detect or filter out third parties from frames
- Obtain consent on your behalf
- Accept responsibility for your capture of others

### 12.3 Recommended Practices

- Use the Application in a private space
- Position your camera to show only your immediate workspace
- Pause sessions when others enter your space
- Inform household members that you use focus tracking software

---

## 13. Children's Privacy

### 13.1 Age Restrictions

The Application is not intended for children under 13 years of age. We do not knowingly collect information from children under 13.

### 13.2 Parental Consent

If you are between 13 and 18 years of age, you must have permission from a parent or guardian to use the Application. The parent or guardian is responsible for:

- Reviewing this Privacy Policy
- Supervising the child's use of the Application
- Ensuring appropriate consent for camera capture

### 13.3 Discovery of Child's Data

If we learn we have collected personal information from a child under 13 without parental consent, we will take steps to delete that information.

---

## 14. Workplace Use

### 14.1 Employee Use

If you use BrainDock on your own initiative for personal productivity at work:
- You are responsible for complying with your employer's policies
- Session data on your work device may be subject to employer access

### 14.2 Employer Deployment

If an employer deploys BrainDock to monitor employees:
- The employer becomes a controller of data collected through the Application
- The employer must provide their own privacy notice to employees
- The employer must comply with workplace surveillance laws
- We are not responsible for the employer's data handling practices

**This Privacy Policy applies to our direct relationship with users, not to employer-employee relationships.**

---

## 15. Cookies and Tracking

The desktop Application does not use cookies or web tracking technologies.

If you visit any associated websites, those sites may use cookies as described in their respective privacy notices.

---

## 16. Changes to This Privacy Policy

### 16.1 Updates

We may update this Privacy Policy from time to time. Changes will be indicated by the "Last Updated" date at the top.

### 16.2 Notification

For material changes, we will notify you through:
- In-app notification
- Email (if available)
- Notice on our website

### 16.3 Your Continued Use

Your continued use of the Application after changes constitutes acceptance of the updated Privacy Policy.

---

## 17. Additional Information for Specific Jurisdictions

### 17.1 California Residents (CCPA)

California residents have specific rights under the California Consumer Privacy Act. Contact us for information about exercising these rights.

### 17.2 Other Jurisdictions

If you are located in a jurisdiction with specific privacy laws not addressed here, please contact us to discuss how we can accommodate your rights.

---

## 18. Data Flow Summary

For transparency, here is a summary of how data flows through our Application:

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR DEVICE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CAMERA MONITORING (always on during sessions)                   │
│  Camera → Captures frames → Sent to AI → Returns presence info   │
│                                                                  │
│  SCREEN MONITORING (always on during sessions)                   │
│  Window titles & URLs → Checked locally against your blocklist   │
│  (NOT sent to AI unless screenshot analysis enabled)             │
│                                                                  │
│  SCREENSHOT ANALYSIS (optional, disabled by default)             │
│  If enabled: Screenshot → Sent to AI → Returns distraction info  │
│  (Screenshots are NOT stored)                                    │
│                                                                  │
│  Results stored locally → Session logs, statistics               │
│       ↓                                                          │
│  PDF Report generated → Saved to Downloads folder                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              AI PROVIDERS (One used at a time)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  OPENAI                         GOOGLE GEMINI                    │
│  • Vision API                   • Gemini Vision API              │
│  • Located in US                • Located in US                  │
│  • Up to 30 days retention      • Per Google's policy            │
│  • No training on API data      • No training on API data        │
│                                                                  │
│  Both providers receive:                                         │
│  • Camera frames (for presence/gadget detection)                 │
│  • Screenshots if enabled (for distraction detection)            │
│  • Return detection results only                                 │
│  • Do not use API data for model training                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

Data NOT Collected:
✗ Biometric templates
✗ Facial recognition data  
✗ Audio recordings
✗ Keystroke data
✗ File contents
✗ Passwords or sensitive text from screenshots
```

---

## 19. Questions and Contact

If you have questions about this Privacy Policy or our data practices, please contact us:

**Email:** morayyajain@gmail.com

**Website:** thebraindock.com

**Address:** 108-128 Leicester Street, Carlton, VIC-3053

We aim to respond to all enquiries within 30 days.

---

## 20. Acknowledgment

By using BrainDock, you acknowledge that you have read and understood this Privacy Policy and consent to the collection, use, and disclosure of your information as described herein.

---

*This Privacy Policy was last updated in January 2026.*

*This policy is designed to comply with the Australian Privacy Act 1988 and Australian Privacy Principles (APPs), GDPR, and UK GDPR. However, this document does not constitute legal advice. We recommend consulting with a qualified privacy lawyer for advice specific to your situation.*
