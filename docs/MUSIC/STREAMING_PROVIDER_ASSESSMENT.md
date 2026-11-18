# JUSTBADDO — STREAMING PROVIDER RESEARCH & SELECTION ASSESSMENT

## 1. Executive Summary

This assessment evaluates potential streaming providers and audio delivery pathways for JustBaddo against legal, technical, operational, and commercial criteria.

JustBaddo's core requirement is to enable fan discovery and playback of Olamide's catalogue through its custom interface without hosting unlicensed recordings or infringing rightsholders' master and publishing rights.

---

## 2. Comprehensive Provider Evaluation Matrix

| Evaluation Criteria | SoundCloud (Widget API) | YouTube (IFrame API) | Spotify (Web Playback SDK) | Apple Music (MusicKit JS) | Audiomack (API & Widget) | Direct Licensed CDN (Phase 7) |
|---|---|---|---|---|---|---|
| **1. API Availability** | Publicly accessible via Widget JS API. | Publicly accessible via IFrame JS API. | Public API with developer registration. | Public JS library requiring Apple Dev account. | Developer API & embed player. | Self-managed via S3/R2 & CloudFront. |
| **2. Commercial Usage** | Non-commercial embeds permitted; commercial requires Partner tier. | Standard embeds permitted; ad monetisation retained by YouTube. | Strictly non-commercial for third-party embeds. | Permitted under Apple Developer Terms. | Partnership required for monetization. | **Fully permitted** under direct label agreements. |
| **3. In-App Playback** | **Yes** (via invisible or styled iframe widget). | **Yes** (requires visible video/visualizer frame). | **Yes** (via browser Web Playback SDK). | **Yes** (via HTML5 audio instance). | **Yes** (via embed widget). | **Yes** (native HTML5 `<audio>` / HLS). |
| **4. Territories (Nigeria & Global)** | Global, including Nigeria and diaspora. | Worldwide coverage, rightsholder-managed geo-filtering. | Worldwide, requires user region matching. | Worldwide, requires user Apple Music region. | Exceptional coverage across Nigeria & West Africa. | **Controlled directly** via geo-DNS / IP headers. |
| **5. Audio Quality** | 128 kbps AAC / 64 kbps Opus. | 128 kbps – 256 kbps AAC (video stream). | 256 kbps – 320 kbps Ogg/AAC. | 256 kbps AAC / Lossless ALAC. | 160 kbps – 320 kbps MP3/AAC. | **Configurable** up to 320 kbps AAC / FLAC. |
| **6. User Authentication** | **None required** for public embed tracks. | **None required** for public video playback. | **Mandatory** active Spotify Premium account login. | **Mandatory** active Apple Music subscription login. | **None required** for basic stream embeds. | **None required** for free tier; JustBaddo JWT for premium. |
| **7. Playback Restrictions** | Rightsholder can disable third-party embedding. | Embedding must show player frame; cannot strip audio only. | Free tier Spotify users cannot stream via SDK. | Non-subscribers limited to 30-second previews. | Rightsholder embed permissions apply. | Fully governed by executed contract terms. |
| **8. Rate Limits** | High capacity on widget iframe; 15,000 req/day on REST API. | 10,000 quota units/day on YouTube Data API. | Standard DRF-compatible rate limits. | Standard Apple Music token limits. | Standard API rate limits. | **Virtually unlimited** (governed by CDN capacity). |
| **9. Attribution Requirements** | SoundCloud logo and track link required in widget. | YouTube watermark and branding displayed in iframe. | Spotify branding and green play pill required. | Apple Music badge and typography required. | Audiomack logo and artist link. | **JustBaddo primary branding** + statutory copyright notices. |
| **10. Revenue Sharing** | None for basic embeds; Partner revenue share required. | Ad revenue flows directly to YBNL / EMPIRE via Content ID. | None; Spotify retains all subscriber fees. | None; Apple retains subscription fees. | Monetization program available for partners. | **Direct royalty accounting** paid to rightsholders. |
| **11. Developer Access** | Instant access for widget; partner review for API. | Google Cloud Console project creation. | Spotify Developer Dashboard registration. | Paid Apple Developer Program ($99/year). | Developer portal application. | AWS / Cloudflare infrastructure credentials. |
| **12. Long-Term Reliability** | High (established standard). | Very High (Google global infrastructure). | Very High. | Very High. | High (strong Afrobeats presence). | **Highest** (platform owns delivery pipeline). |
| **13. UI Control from JustBaddo** | **High** (play, pause, seek, volume, progress events via JS). | **High** (full JS player API with play, pause, seek, volume). | **Full** (headless audio player controlled via JS). | **Full** (headless audio player controlled via JS). | Moderate (limited iframe widget events). | **Complete** (full HTML5 audio element control). |
| **14. Free vs Future Premium** | **Compatible** with free discovery. | **Compatible** with free discovery. | **Incompatible** with free anonymous visitors. | **Incompatible** with free anonymous visitors. | **Compatible** with free discovery. | **Optimal** (platform gates tiers directly). |

---

## 3. Provider Selection & Strategic Decision

### Selected Initial Providers:
1. **Primary Streaming Sources:**
   - **SoundCloud Widget API:** For official Olamide releases and YBNL tracks that allow embed streaming.
   - **YouTube IFrame Player API:** For official music videos and audio visualizers released on the verified Olamide / YBNL YouTube channels. Provides complete catalogue coverage for tracks with official video uploads.
2. **Development & Offline Fallback:**
   - **Web Audio API Synth (`MockAudioProvider`):** Generates zero-copyright rhythmic harmonic pulses keyed to track BPM and key. Guarantees uninterrupted queue advancement during local testing or partner network dropouts.
3. **Long-Term Target (Phase 7):**
   - **JustBaddo Direct Licensed CDN (`SelfHostedAudioProvider`):** Prepares the codebase for direct HLS chunk delivery upon execution of formal master and publishing agreements.

---

## 4. Legal Compliance & Verified vs Pending Permissions

> [!IMPORTANT]
> **Clearance Status Declaration:**
> - JustBaddo **does not** hold direct commercial synchronization or master redistribution licenses from EMPIRE or YBNL Nation.
> - Current playback relies strictly on **authorized third-party embed widgets** complying with SoundCloud and YouTube public embedding terms.
> - Direct file hosting or audio re-streaming remains **strictly disabled** until Phase 6 licensing outreach is executed.

| Integration Channel | Verified Capability | Outstanding / Pending Legal Clearance |
|---|---|---|
| **SoundCloud Widget** | Standard embed player functioning under public widget terms. | Commercial Partner Agreement for headless/custom audio player skins. |
| **YouTube IFrame** | Official visualizer playback embedded in player slot. | Written waiver for headless audio-only streaming (strictly prohibited by YouTube TOS). |
| **Web Audio API Synth** | 100% legal, zero-copyright synthetic sound generation. | None (self-generated mathematical waveforms). |
| **Self-Hosted CDN** | Technical adapter implemented and unit-tested. | Master recording license (EMPIRE/YBNL) and mechanical publishing license (COSON/MCSN/Publishers). |
