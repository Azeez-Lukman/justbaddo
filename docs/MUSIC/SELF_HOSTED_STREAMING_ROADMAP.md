# JUSTBADDO — SELF-HOSTED DIRECT STREAMING ROADMAP (PHASE 7 PREPARATION)

## 1. Vision & Strategic Objective

When JustBaddo secures direct mechanical and master streaming agreements with Olamide's label representatives (YBNL Nation and EMPIRE), the platform will transition from external third-party embed widgets to an independent, high-performance, self-hosted streaming infrastructure.

This document establishes the technical blueprint, media processing pipeline, security protocols, and cost models required for Phase 7 implementation.

> [!CAUTION]
> **Strict Prerequisite Notice:**
> - Direct audio delivery must **never** be activated using unlicensed master files.
> - No cloud storage, transcoding servers, or CDN subscriptions will be purchased prior to formal legal execution and explicit administrative approval.

---

## 2. Target Phase 7 Audio Delivery Architecture

```mermaid
flowchart TD
    MasterAudio["Authorized Master Recordings (FLAC/WAV)"] --> Transcode["Automated Transcoding Worker (FFmpeg / HLS Segmenter)"]
    Transcode --> MasterHLS["Multi-Bitrate HLS Chunks (.m3u8 + .ts segments)"]
    MasterHLS --> PrivateStorage[("Encrypted Private Object Storage (Cloudflare R2 / AWS S3)")]
    
    Client["JustBaddo Web App / Player"] -->|POST /session/| DjangoAPI["Django Playback API Gateway"]
    DjangoAPI -->|Verify Rights & Territory| TokenSigner["HMAC Signed URL Generator (15-min TTL)"]
    TokenSigner -->> Client: Secure Media Token
    
    Client -->|GET /stream/<track_id>.m3u8?token=...| EdgeCDN["Global Edge CDN (Cloudflare / AWS CloudFront)"]
    EdgeCDN -->|Validate Token & Cache Chunks| PrivateStorage
    EdgeCDN -->> Client: Encrypted HLS Adaptive Stream
```

---

## 3. Media Processing Pipeline

### 3.1. Audio Transcoding & Adaptive Bitrate Streaming (HLS)
Raw studio recordings will be encoded into three bandwidth-optimized tiers using FFmpeg:

| Audio Tier | Target Bitrate | Codec | Intended Network Profile |
|---|---|---|---|
| **Low (Mobile Saver)** | 64 kbps | AAC-HE (v2) | 2G/3G mobile networks in low-bandwidth regions |
| **Standard (Default)** | 160 kbps | AAC-LC | 4G/LTE mobile networks, standard desktop listening |
| **High (Audiophile)** | 320 kbps | AAC-LC | Wi-Fi, broadband, premium subscriber tier |

### 3.2. Sample FFmpeg Transcoding Recipe
```bash
# Segment audio into 6-second encrypted HLS segments
ffmpeg -i master_track.wav \
  -c:a aac -b:a 160k -ar 44100 -ac 2 \
  -f hls -hls_time 6 -hls_playlist_type vod \
  -hls_segment_filename "track_160k_%03d.ts" \
  track_160k.m3u8
```

---

## 4. Security & DRM Tokenization

1. **Private Bucket Policy:**
   The storage bucket has zero public access. All origin requests are restricted to Cloudflare R2 / CloudFront Origin Access Identity (OAI).
2. **HMAC Signed URLs:**
   Audio segments are accessed via signed query tokens with a 15-minute Time-To-Live (TTL):
   ```python
   # Example signature generation in Django
   import hmac, hashlib, time
   token = hmac.new(SECRET_KEY.encode(), f"{track_id}:{expires}:{user_id}".encode(), hashlib.sha256).hexdigest()
   ```
3. **Geo-IP Enforcement at Edge:**
   The CDN edge worker parses the client's country header and rejects requests originating from unauthorized territories with HTTP 403 Forbidden before fetching audio chunks.

---

## 5. Bandwidth & Operating Cost Projections (at Scale)

*Based on Cloudflare R2 ($0 egress fees) + Cloudflare Stream / Workers:*

| Scale Metric | 10,000 MAU | 50,000 MAU | 200,000 MAU |
|---|---|---|---|
| **Monthly Stream Hours** | 25,000 hrs | 150,000 hrs | 750,000 hrs |
| **Data Transfer (160kbps)** | 1.8 TB | 10.8 TB | 54.0 TB |
| **Storage (150 tracks)** | ~12 GB | ~12 GB | ~12 GB |
| **Estimated R2 Storage Cost**| $0.18 / mo | $0.18 / mo | $0.18 / mo |
| **CDN Egress Bandwidth** | $0.00 (Cloudflare R2) | $0.00 (Cloudflare R2) | $0.00 (Cloudflare R2) |
| **Total Audio Delivery Cost**| **~$5.00 – $15.00 / mo** | **~$20.00 – $45.00 / mo** | **~$75.00 – $160.00 / mo** |
