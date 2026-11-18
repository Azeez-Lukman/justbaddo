# JUSTBADDO — PHASE 6: AUTHORISED MUSIC STREAMING & PLAYER ACTIVATION

## PROJECT OBJECTIVE

Implement a production-oriented, provider-independent music playback system for JustBaddo.

JustBaddo is an independent music discovery and fan community platform dedicated to Olamide Baddo. Its music experience should allow users to discover music, interact with the catalogue and play authorised recordings through the existing JustBaddo interface.

The objective of this phase is to activate the existing music player through a properly authorised streaming source while preparing the architecture for future direct licensing and self-hosted audio delivery.

This is not a frontend redesign. It is a focused extension of the existing application.

## 1. MANDATORY PRE-IMPLEMENTATION AUDIT

Before writing or modifying code:

1. Inspect the complete existing project structure.
2. Read README.md, PROJECT_STATUS.md, TODO.md, RECOMMENDATION.md and all relevant music, backend, database, testing and deployment documentation.
3. Inspect the existing Django music, playback and licensing applications.
4. Inspect all existing music models, serializers, views, services, API endpoints and permissions.
5. Inspect the frontend player implementation, including:
   - Player state management.
   - Audio element or playback abstraction.
   - Queue management.
   - Play/pause controls.
   - Previous/next controls.
   - Progress and seeking.
   - Volume controls.
   - Expanded player.
   - Persistent navigation behaviour.
6. Inspect the existing API client and authentication implementation.
7. Run the current automated test suite and record its baseline.
8. Identify existing functionality that can be reused.

Do not recreate existing functionality unnecessarily.

Do not introduce breaking changes to Phases 1–5.

Do not assume that an external provider has already granted JustBaddo streaming rights.

## 2. STREAMING PROVIDER RESEARCH AND SELECTION

Investigate possible authorised streaming integrations.

Evaluate providers against:

- API availability.
- Commercial usage permissions.
- In-app playback permissions.
- Supported territories.
- Audio quality.
- Authentication requirements.
- Playback restrictions.
- API rate limits.
- Attribution requirements.
- Revenue-sharing conditions.
- Developer access requirements.
- Long-term reliability.
- Whether playback can be controlled through JustBaddo's interface.
- Whether the provider permits the intended free and future premium model.

Investigate suitable providers and licensing pathways, including relevant music streaming APIs and authorised embeddable players.

Do not assume that an API, embed, public streaming URL or existing subscription grants permission to redistribute or re-stream recordings.

IMPORTANT:

If no provider offers sufficient permissions for the intended integration, document the limitation and implement a provider adapter that can be activated once an appropriate agreement is secured.

Do not bypass provider restrictions, scrape audio, extract protected streams or proxy unauthorised audio.

Do not use unofficial MP3 links.

## 3. PROVIDER-INDEPENDENT PLAYBACK ARCHITECTURE

Implement a provider-independent architecture.

The core JustBaddo player must not depend directly on one provider's implementation.

Create or extend a provider interface responsible for:

- Initialising playback.
- Starting a track.
- Pausing playback.
- Resuming playback.
- Stopping playback.
- Seeking where supported.
- Retrieving playback state.
- Handling track completion.
- Handling provider errors.
- Handling unavailable tracks.
- Reporting supported playback capabilities.

Provider-specific implementations must be isolated from the core playback application.

A provider must be replaceable without rebuilding the entire player.

Use the existing Django modular monolith and frontend architecture.

Do not introduce unnecessary microservices.

## 4. BACKEND IMPLEMENTATION

Extend the existing Django applications.

Review and improve the following areas:

### Music application

Ensure each track has sufficient metadata to support playback decisions.

Preserve existing catalogue records and relationships.

Track metadata should support:

- Track title.
- Album.
- Artist.
- Duration.
- Track number.
- Cover artwork.
- Release information.
- Playback status.
- Provider association.
- Provider track identifier.
- Availability territories.
- Rights status.

### Playback application

Implement or improve:

- Playback session creation.
- Playback session validation.
- Provider resolution.
- Playback event handling.
- Listening history.
- Completion tracking.
- Playback error logging.
- Supported playback capabilities.

Playback sessions must only be created for tracks with an authorised playback source.

### Licensing application

Make licensing records central to playback eligibility.

Support:

- Rights verification.
- Master recording permissions.
- Composition and publishing permissions where applicable.
- Provider permissions.
- Territory restrictions.
- Start and expiration dates.
- Commercial usage permissions.
- Free and premium usage permissions.
- Explicit playback approval.
- Rights withdrawal.

A track must never become playable merely because its metadata or provider URL exists.

### Permissions and security

Ensure users cannot:

- Access restricted recordings through manipulated requests.
- Bypass territory restrictions.
- Create unauthorised playback sessions.
- Submit fabricated playback completion events.
- Access another user's private listening history.
- Manipulate licensing records.

Use server-side validation for all important playback decisions.

## 5. FRONTEND PLAYER ACTIVATION

Connect the existing frontend player to the authorised playback architecture.

Preserve the existing design system and visual identity.

Implement or verify:

- Play and pause.
- Previous and next.
- Track progress.
- Seeking where supported.
- Volume.
- Mute.
- Queue.
- Expanded player.
- Track artwork.
- Track and artist information.
- Loading states.
- Buffering states.
- Playback errors.
- Unavailable track states.
- Empty queue states.
- Mobile player behaviour.
- Persistent playback state during supported navigation.

The interface should remain simple, premium, responsive and self-explanatory.

Do not redesign unrelated pages.

The player must never display a successful playback state when the provider has not confirmed playback.

## 6. PLAYBACK AVAILABILITY AND FALLBACK

Introduce clear playback availability states.

At minimum:

- metadata_only
- provider_available
- self_hosted_available
- restricted
- withdrawn

The interface should respond appropriately to each state.

For example:

- Metadata-only tracks can be explored but not played.
- Provider-available tracks can play through an authorised provider.
- Self-hosted tracks can play only through an authorised JustBaddo audio source.
- Restricted tracks must not start playback.
- Withdrawn tracks must immediately become unavailable.

Handle provider outages gracefully.

Do not silently substitute an unrelated recording.

## 7. LISTENING HISTORY AND ANALYTICS

Connect authorised playback events to the existing PostgreSQL listening history.

Record meaningful events, including:

- Playback started.
- Playback paused.
- Playback resumed.
- Playback completed.
- Playback failed.
- Playback position where appropriate.

Prevent fabricated completion events and duplicate submissions.

Respect privacy settings, including the user's listening-history visibility preference.

Do not expose private listening information to other users.

## 8. FUTURE SELF-HOSTED STREAMING PREPARATION

Prepare the architecture for a future stage in which JustBaddo obtains direct licences and hosts authorised audio files.

Document a possible architecture involving:

- Private object storage.
- Secure audio delivery.
- CDN distribution.
- Signed or time-limited playback access.
- Rights-aware delivery.
- Territory enforcement.
- Playback analytics.
- Storage and bandwidth monitoring.

Do not upload commercial recordings or build public audio delivery around unlicensed files.

Do not purchase hosting, storage or CDN services without explicit approval.

## 9. TESTING REQUIREMENTS

Create comprehensive tests for:

- Provider adapter behaviour.
- Provider initialisation.
- Playback session creation.
- Track availability.
- Rights validation.
- Territory restrictions.
- Expired permissions.
- Withdrawn recordings.
- Authentication.
- Playback permissions.
- Provider failures.
- Queue behaviour.
- Listening-history recording.
- Duplicate completion events.
- Frontend playback states.
- Mobile responsiveness.

Run the existing test suite as regression testing.

Do not report tests as passing unless they have actually been executed.

## 10. DOCUMENTATION

Create the following documentation:

docs/music/
- PHASE_6_README.md
- STREAMING_PROVIDER_ASSESSMENT.md
- PLAYBACK_ARCHITECTURE.md
- PROVIDER_INTEGRATION.md
- PLAYBACK_API.md
- LICENSING_AND_RIGHTS_CHECKLIST.md
- SELF_HOSTED_STREAMING_ROADMAP.md

docs/testing/
- Update TEST_CASES.md.
- Update BUG_TRACKER.md.
- Update INTEGRATION_REPORT.md with Phase 6 results.

Update the root files:

- README.md
- TODO.md
- PROJECT_STATUS.md
- RECOMMENDATION.md

Document all implementation decisions, limitations, environment variables, provider dependencies and setup instructions.

## 11. IMPLEMENTATION RULES

- Preserve existing working functionality.
- Do not delete existing migrations or reset the database.
- Do not hardcode API credentials.
- Use environment variables for secrets.
- Do not invent provider permissions.
- Do not use unlicensed recordings.
- Do not expose private provider credentials in frontend code.
- Follow the existing coding conventions.
- Keep the application modular.
- Avoid unnecessary dependencies.
- Do not introduce a new frontend framework.
- Maintain compatibility with PostgreSQL 18.
- Keep all changes under Git version control.

If an external provider account, API key, legal agreement or commercial permission is required, clearly identify the requirement and provide the integration interface without pretending that access has been granted.

## 12. PHASE 6 COMPLETION CRITERIA

Phase 6 can only be marked complete when:

1. The existing playback architecture has been audited.
2. The provider assessment has been documented.
3. The provider adapter architecture is implemented.
4. An authorised playback source has been integrated or the integration is explicitly marked blocked pending external approval.
5. The existing JustBaddo player is connected to the playback architecture.
6. Track availability and licensing restrictions are enforced server-side.
7. Listening history is correctly integrated.
8. Playback failures are handled gracefully.
9. Automated tests have been executed and their results documented.
10. Existing Phase 1–5 functionality remains intact.
11. All required documentation is updated.
12. Git changes are committed.

IMPORTANT FINAL REPORT:

At completion, provide:

- What was implemented.
- Files created and modified.
- Provider selected and the basis for selection.
- Provider permissions verified versus still pending.
- API endpoints created or updated.
- Database changes and migrations.
- Automated test results.
- Manual playback verification results.
- Outstanding external requirements.
- Security and licensing limitations.
- Git commit reference.
- Recommended next phase.

Do not claim that real Olamide recordings are playable unless the relevant permissions and playback access have actually been secured.

Begin with the audit, then proceed systematically through implementation and verification.