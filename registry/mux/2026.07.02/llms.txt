# Mux Documentation for LLMs

> Mux is how developers build online video. Mux provides a complete video platform that includes:
> - Video hosting, encoding, and streaming infrastructure
> - A modern, responsive video player with adaptive controls
> - Video analytics and performance monitoring
> - all with a great developer experience and surprisingly affordable pricing

## Quick start: What are you trying to do?

- **Upload and stream a video file** → Start with /docs/core.txt, then /docs/guides/video.txt
- **Build a video player** → /docs/guides/player.txt
- **Handle file uploads from users** → /docs/guides/uploader.txt
- **Track playback metrics and analytics** → /docs/guides/data.txt
- **Set up a live stream** → /docs/core.txt (live streams section) + /docs/guides/video.txt
- **Integrate with a web framework (Next.js, Rails, etc.)** → /docs/integrations.txt
- **Need the full API reference** → /api-spec.json

## Common mistakes to avoid

- **Never expose Mux API credentials in client-side code.** All API calls must come from a server. Use direct uploads or signed URLs for client-side operations.
- **Don't poll the assets endpoint to check status.** Use webhooks instead. The `video.asset.ready` event tells you when an asset is ready for playback.
- **Don't confuse Asset IDs with Playback IDs.** Asset IDs (used with api.mux.com) are for managing assets. Playback IDs (used with stream.mux.com) are for streaming to viewers.
- **Don't expose stream keys in public code.** Treat stream keys like passwords. Anyone with the key can broadcast to your live stream.
- **Don't hardcode playback URLs.** Playback IDs can change. Store the asset ID and look up playback IDs when needed, or store playback IDs separately.

## For AI agents

If you're an AI agent that can use MCP (Model Context Protocol) tools, the Mux MCP server provides direct API access for video uploads, live streaming, and analytics queries.

- Hosted MCP: https://mcp.mux.com
- GitHub: https://github.com/muxinc/mux-node-sdk/tree/master/packages/mcp-server/vercel-function
- Setup guide: /docs/integrations/mcp-server.md

## Notes

- All documentation is automatically generated from the same source as our official documentation
- API specifications include detailed endpoint descriptions, request/response formats, and examples following the OpenAPI specification
- The documentation is regularly updated to reflect the latest features and capabilities
- API version: v1 (stable)
- Player version: @mux/mux-player 3.x, @mux/mux-player-react 3.x

## Guide collections

- [/docs/core.txt](https://www.mux.com/docs/core.txt): Core Mux concepts (start here for most projects)
- [/llms-full.txt](https://www.mux.com/llms-full.txt): All Mux docs in one file (if your context window is large enough)
- [/docs/guides/video.txt](https://www.mux.com/docs/guides/video.txt): Upload, encode, and manage video assets
- [/docs/guides/uploader.txt](https://www.mux.com/docs/guides/uploader.txt): Handle user uploads from browsers and mobile apps
- [/docs/guides/player.txt](https://www.mux.com/docs/guides/player.txt): Embed video playback with Mux Player
- [/docs/guides/data.txt](https://www.mux.com/docs/guides/data.txt): Track playback quality and viewer analytics
- [/docs/guides/data-integrations.txt](https://www.mux.com/docs/guides/data-integrations.txt): Add Mux Data to third-party players (Video.js, HLS.js, etc.)
- [/docs/integrations.txt](https://www.mux.com/docs/integrations.txt): Framework guides (Next.js, Rails, Laravel, etc.) and SDKs
- [/docs/examples.txt](https://www.mux.com/docs/examples.txt): Example implementations and use cases
- [/docs/pricing.txt](https://www.mux.com/docs/pricing.txt): Pricing and billing information

## API references

- [/docs/api-reference/system.txt](https://www.mux.com/docs/api-reference/system.txt): Mux system API specification
- [/docs/api-reference/video.txt](https://www.mux.com/docs/api-reference/video.txt): Mux Video API specification
- [/docs/api-reference/data.txt](https://www.mux.com/docs/api-reference/data.txt): Mux Data API specification
- [/api-spec.json](https://www.mux.com/api-spec.json): Complete Mux API reference
- [/webhook-spec.json](https://www.mux.com/webhook-spec.json): Complete Mux Webhook reference

### External API references

- [https://raw.githubusercontent.com/muxinc/elements/refs/heads/main/packages/mux-player/REFERENCE.md](https://raw.githubusercontent.com/muxinc/elements/refs/heads/main/packages/mux-player/REFERENCE.md): Mux Player Web Component API reference
- [https://raw.githubusercontent.com/muxinc/elements/refs/heads/main/packages/mux-player-react/REFERENCE.md](https://raw.githubusercontent.com/muxinc/elements/refs/heads/main/packages/mux-player-react/REFERENCE.md): Mux Player React Component API reference

## All guides

- [/docs/core/stream-video-files.md](https://www.mux.com/docs/core/stream-video-files.md)
- [/docs/core/mux-fundamentals.md](https://www.mux.com/docs/core/mux-fundamentals.md)
- [/docs/core/ai-agents.md](https://www.mux.com/docs/core/ai-agents.md)
- [/docs/core/make-api-requests.md](https://www.mux.com/docs/core/make-api-requests.md)
- [/docs/core/sdks.md](https://www.mux.com/docs/core/sdks.md)
- [/docs/core/postman.md](https://www.mux.com/docs/core/postman.md)
- [/docs/core/listen-for-webhooks.md](https://www.mux.com/docs/core/listen-for-webhooks.md)
- [/docs/core/verify-webhook-signatures.md](https://www.mux.com/docs/core/verify-webhook-signatures.md)
- [/docs/core/content-security-policy.md](https://www.mux.com/docs/core/content-security-policy.md)
- [/docs/guides/migrate-from-self-managed.md](https://www.mux.com/docs/guides/migrate-from-self-managed.md)
- [/docs/guides/mux-uploader.md](https://www.mux.com/docs/guides/mux-uploader.md)
- [/docs/guides/uploader-web-core-functionality.md](https://www.mux.com/docs/guides/uploader-web-core-functionality.md)
- [/docs/guides/uploader-web-integrate-in-your-webapp.md](https://www.mux.com/docs/guides/uploader-web-integrate-in-your-webapp.md)
- [/docs/guides/uploader-web-customize-look-and-feel.md](https://www.mux.com/docs/guides/uploader-web-customize-look-and-feel.md)
- [/docs/guides/uploader-web-use-subcomponents-directly.md](https://www.mux.com/docs/guides/uploader-web-use-subcomponents-directly.md)
- [/docs/guides/use-video-quality-levels.md](https://www.mux.com/docs/guides/use-video-quality-levels.md)
- [/docs/guides/stream-videos-in-4k.md](https://www.mux.com/docs/guides/stream-videos-in-4k.md)
- [/docs/guides/upload-files-directly.md](https://www.mux.com/docs/guides/upload-files-directly.md)
- [/docs/guides/upload-video-directly-from-android.md](https://www.mux.com/docs/guides/upload-video-directly-from-android.md)
- [/docs/guides/upload-video-directly-from-ios-or-ipados.md](https://www.mux.com/docs/guides/upload-video-directly-from-ios-or-ipados.md)
- [/docs/guides/minimize-processing-time.md](https://www.mux.com/docs/guides/minimize-processing-time.md)
- [/docs/guides/control-recording-resolution.md](https://www.mux.com/docs/guides/control-recording-resolution.md)
- [/docs/guides/play-your-videos.md](https://www.mux.com/docs/guides/play-your-videos.md)
- [/docs/guides/mux-player-web.md](https://www.mux.com/docs/guides/mux-player-web.md)
- [/docs/guides/player-core-functionality.md](https://www.mux.com/docs/guides/player-core-functionality.md)
- [/docs/guides/player-integrate-in-your-webapp.md](https://www.mux.com/docs/guides/player-integrate-in-your-webapp.md)
- [/docs/guides/player-customize-look-and-feel.md](https://www.mux.com/docs/guides/player-customize-look-and-feel.md)
- [/docs/guides/player-themes.md](https://www.mux.com/docs/guides/player-themes.md)
- [/docs/guides/player-lazy-loading.md](https://www.mux.com/docs/guides/player-lazy-loading.md)
- [/docs/guides/player-ads.md](https://www.mux.com/docs/guides/player-ads.md)
- [/docs/guides/player-advanced-usage.md](https://www.mux.com/docs/guides/player-advanced-usage.md)
- [/docs/guides/player-examples.md](https://www.mux.com/docs/guides/player-examples.md)
- [/docs/guides/player-faqs.md](https://www.mux.com/docs/guides/player-faqs.md)
- [/docs/guides/player-releases-web.md](https://www.mux.com/docs/guides/player-releases-web.md)
- [/docs/guides/mux-player-ios.md](https://www.mux.com/docs/guides/mux-player-ios.md)
- [/docs/guides/player-releases-ios.md](https://www.mux.com/docs/guides/player-releases-ios.md)
- [/docs/guides/mux-player-android.md](https://www.mux.com/docs/guides/mux-player-android.md)
- [/docs/guides/player-releases-android.md](https://www.mux.com/docs/guides/player-releases-android.md)
- [/docs/guides/mux-background-video.md](https://www.mux.com/docs/guides/mux-background-video.md)
- [/docs/guides/control-playback-resolution.md](https://www.mux.com/docs/guides/control-playback-resolution.md)
- [/docs/guides/web-autoplay-your-videos.md](https://www.mux.com/docs/guides/web-autoplay-your-videos.md)
- [/docs/guides/use-a-custom-domain-for-streaming.md](https://www.mux.com/docs/guides/use-a-custom-domain-for-streaming.md)
- [/docs/guides/embed-videos-for-social-media.md](https://www.mux.com/docs/guides/embed-videos-for-social-media.md)
- [/docs/guides/enable-static-mp4-renditions.md](https://www.mux.com/docs/guides/enable-static-mp4-renditions.md)
- [/docs/guides/download-for-offline-editing.md](https://www.mux.com/docs/guides/download-for-offline-editing.md)
- [/docs/guides/get-images-from-a-video.md](https://www.mux.com/docs/guides/get-images-from-a-video.md)
- [/docs/guides/create-timeline-hover-previews.md](https://www.mux.com/docs/guides/create-timeline-hover-previews.md)
- [/docs/guides/playback-videojs-with-mux.md](https://www.mux.com/docs/guides/playback-videojs-with-mux.md)
- [/docs/guides/modify-playback-behavior.md](https://www.mux.com/docs/guides/modify-playback-behavior.md)
- [/docs/guides/add-metadata-to-your-videos.md](https://www.mux.com/docs/guides/add-metadata-to-your-videos.md)
- [/docs/guides/add-autogenerated-captions-and-use-transcripts.md](https://www.mux.com/docs/guides/add-autogenerated-captions-and-use-transcripts.md)
- [/docs/guides/add-subtitles-to-your-videos.md](https://www.mux.com/docs/guides/add-subtitles-to-your-videos.md)
- [/docs/guides/add-alternate-audio-tracks-to-your-videos.md](https://www.mux.com/docs/guides/add-alternate-audio-tracks-to-your-videos.md)
- [/docs/guides/intro-to-clips.md](https://www.mux.com/docs/guides/intro-to-clips.md)
- [/docs/guides/create-instant-clips.md](https://www.mux.com/docs/guides/create-instant-clips.md)
- [/docs/guides/create-clips-from-your-videos.md](https://www.mux.com/docs/guides/create-clips-from-your-videos.md)
- [/docs/guides/add-watermarks-to-your-videos.md](https://www.mux.com/docs/guides/add-watermarks-to-your-videos.md)
- [/docs/guides/adjust-audio-levels.md](https://www.mux.com/docs/guides/adjust-audio-levels.md)
- [/docs/guides/find-different-shots-in-your-video.md](https://www.mux.com/docs/guides/find-different-shots-in-your-video.md)
- [/docs/guides/robots.md](https://www.mux.com/docs/guides/robots.md)
- [/docs/guides/robots-directives.md](https://www.mux.com/docs/guides/robots-directives.md)
- [/docs/guides/robots-summarize.md](https://www.mux.com/docs/guides/robots-summarize.md)
- [/docs/guides/robots-moderate.md](https://www.mux.com/docs/guides/robots-moderate.md)
- [/docs/guides/robots-generate-chapters.md](https://www.mux.com/docs/guides/robots-generate-chapters.md)
- [/docs/guides/robots-ask-questions.md](https://www.mux.com/docs/guides/robots-ask-questions.md)
- [/docs/guides/robots-find-key-moments.md](https://www.mux.com/docs/guides/robots-find-key-moments.md)
- [/docs/guides/robots-translate-captions.md](https://www.mux.com/docs/guides/robots-translate-captions.md)
- [/docs/guides/robots-translate-audio.md](https://www.mux.com/docs/guides/robots-translate-audio.md)
- [/docs/guides/robots-generate-premium-captions.md](https://www.mux.com/docs/guides/robots-generate-premium-captions.md)
- [/docs/guides/robots-edit-captions.md](https://www.mux.com/docs/guides/robots-edit-captions.md)
- [/docs/guides/robots-find-scenes.md](https://www.mux.com/docs/guides/robots-find-scenes.md)
- [/docs/guides/robots-find-best-thumbnails.md](https://www.mux.com/docs/guides/robots-find-best-thumbnails.md)
- [/docs/guides/robots-generate-engagement-insights.md](https://www.mux.com/docs/guides/robots-generate-engagement-insights.md)
- [/docs/guides/start-live-streaming.md](https://www.mux.com/docs/guides/start-live-streaming.md)
- [/docs/guides/configure-broadcast-software.md](https://www.mux.com/docs/guides/configure-broadcast-software.md)
- [/docs/guides/use-srt-to-live-stream.md](https://www.mux.com/docs/guides/use-srt-to-live-stream.md)
- [/docs/guides/live-streaming-from-your-app.md](https://www.mux.com/docs/guides/live-streaming-from-your-app.md)
- [/docs/guides/reduce-live-stream-latency.md](https://www.mux.com/docs/guides/reduce-live-stream-latency.md)
- [/docs/guides/show-live-stream-health-stats.md](https://www.mux.com/docs/guides/show-live-stream-health-stats.md)
- [/docs/guides/manage-stream-keys.md](https://www.mux.com/docs/guides/manage-stream-keys.md)
- [/docs/guides/stream-recordings-of-live-streams.md](https://www.mux.com/docs/guides/stream-recordings-of-live-streams.md)
- [/docs/guides/stream-live-to-3rd-party-platforms.md](https://www.mux.com/docs/guides/stream-live-to-3rd-party-platforms.md)
- [/docs/guides/handle-live-stream-disconnects.md](https://www.mux.com/docs/guides/handle-live-stream-disconnects.md)
- [/docs/guides/stream-simulated-live.md](https://www.mux.com/docs/guides/stream-simulated-live.md)
- [/docs/guides/debug-live-stream-issues.md](https://www.mux.com/docs/guides/debug-live-stream-issues.md)
- [/docs/guides/add-live-captions.md](https://www.mux.com/docs/guides/add-live-captions.md)
- [/docs/guides/add-autogenerated-live-captions.md](https://www.mux.com/docs/guides/add-autogenerated-live-captions.md)
- [/docs/guides/live-streaming-faqs.md](https://www.mux.com/docs/guides/live-streaming-faqs.md)
- [/docs/guides/monitor-html5-video-element.md](https://www.mux.com/docs/guides/monitor-html5-video-element.md)
- [/docs/guides/monitor-hls-js.md](https://www.mux.com/docs/guides/monitor-hls-js.md)
- [/docs/guides/monitor-avplayer.md](https://www.mux.com/docs/guides/monitor-avplayer.md)
- [/docs/guides/monitor-androidx-media3.md](https://www.mux.com/docs/guides/monitor-androidx-media3.md)
- [/docs/guides/monitor-exoplayer.md](https://www.mux.com/docs/guides/monitor-exoplayer.md)
- [/docs/guides/monitor-dash-js.md](https://www.mux.com/docs/guides/monitor-dash-js.md)
- [/docs/guides/monitor-video-js.md](https://www.mux.com/docs/guides/monitor-video-js.md)
- [/docs/guides/monitor-react-native-video.md](https://www.mux.com/docs/guides/monitor-react-native-video.md)
- [/docs/guides/monitor-kaltura-web.md](https://www.mux.com/docs/guides/monitor-kaltura-web.md)
- [/docs/guides/monitor-kaltura-ios.md](https://www.mux.com/docs/guides/monitor-kaltura-ios.md)
- [/docs/guides/monitor-kaltura-android.md](https://www.mux.com/docs/guides/monitor-kaltura-android.md)
- [/docs/guides/monitor-jw-player-web.md](https://www.mux.com/docs/guides/monitor-jw-player-web.md)
- [/docs/guides/monitor-jw-player-ios.md](https://www.mux.com/docs/guides/monitor-jw-player-ios.md)
- [/docs/guides/monitor-android-media-player.md](https://www.mux.com/docs/guides/monitor-android-media-player.md)
- [/docs/guides/monitor-bitmovin-player.md](https://www.mux.com/docs/guides/monitor-bitmovin-player.md)
- [/docs/guides/monitor-bitmovin-android.md](https://www.mux.com/docs/guides/monitor-bitmovin-android.md)
- [/docs/guides/monitor-castlabs-prestoplay-web.md](https://www.mux.com/docs/guides/monitor-castlabs-prestoplay-web.md)
- [/docs/guides/monitor-castlabs-prestoplay-android.md](https://www.mux.com/docs/guides/monitor-castlabs-prestoplay-android.md)
- [/docs/guides/monitor-akamai-media-player.md](https://www.mux.com/docs/guides/monitor-akamai-media-player.md)
- [/docs/guides/monitor-nexplayer.md](https://www.mux.com/docs/guides/monitor-nexplayer.md)
- [/docs/guides/monitor-ooyala-player.md](https://www.mux.com/docs/guides/monitor-ooyala-player.md)
- [/docs/guides/monitor-shaka-player.md](https://www.mux.com/docs/guides/monitor-shaka-player.md)
- [/docs/guides/monitor-theoplayer-web.md](https://www.mux.com/docs/guides/monitor-theoplayer-web.md)
- [/docs/guides/monitor-theoplayer-ios.md](https://www.mux.com/docs/guides/monitor-theoplayer-ios.md)
- [/docs/guides/monitor-theoplayer-android.md](https://www.mux.com/docs/guides/monitor-theoplayer-android.md)
- [/docs/guides/monitor-flowplayer.md](https://www.mux.com/docs/guides/monitor-flowplayer.md)
- [/docs/guides/monitor-brightcove-web.md](https://www.mux.com/docs/guides/monitor-brightcove-web.md)
- [/docs/guides/monitor-brightcove-ios.md](https://www.mux.com/docs/guides/monitor-brightcove-ios.md)
- [/docs/guides/monitor-brightcove-android.md](https://www.mux.com/docs/guides/monitor-brightcove-android.md)
- [/docs/guides/monitor-cts-pdk.md](https://www.mux.com/docs/guides/monitor-cts-pdk.md)
- [/docs/guides/monitor-chromecast.md](https://www.mux.com/docs/guides/monitor-chromecast.md)
- [/docs/guides/monitor-roku.md](https://www.mux.com/docs/guides/monitor-roku.md)
- [/docs/guides/monitor-samsung-tizen.md](https://www.mux.com/docs/guides/monitor-samsung-tizen.md)
- [/docs/guides/monitor-lg.md](https://www.mux.com/docs/guides/monitor-lg.md)
- [/docs/guides/monitor-agnoplay-player.md](https://www.mux.com/docs/guides/monitor-agnoplay-player.md)
- [/docs/guides/understand-metric-definitions.md](https://www.mux.com/docs/guides/understand-metric-definitions.md)
- [/docs/guides/monitoring-metrics.md](https://www.mux.com/docs/guides/monitoring-metrics.md)
- [/docs/guides/data-engagement-metric.md](https://www.mux.com/docs/guides/data-engagement-metric.md)
- [/docs/guides/data-overall-viewer-experience-metric.md](https://www.mux.com/docs/guides/data-overall-viewer-experience-metric.md)
- [/docs/guides/data-playback-success-metric.md](https://www.mux.com/docs/guides/data-playback-success-metric.md)
- [/docs/guides/data-startup-time-metric.md](https://www.mux.com/docs/guides/data-startup-time-metric.md)
- [/docs/guides/data-smoothness-metric.md](https://www.mux.com/docs/guides/data-smoothness-metric.md)
- [/docs/guides/data-video-quality-metric.md](https://www.mux.com/docs/guides/data-video-quality-metric.md)
- [/docs/guides/make-your-data-actionable-with-metadata.md](https://www.mux.com/docs/guides/make-your-data-actionable-with-metadata.md)
- [/docs/guides/extend-data-with-custom-metadata.md](https://www.mux.com/docs/guides/extend-data-with-custom-metadata.md)
- [/docs/guides/filter-your-data.md](https://www.mux.com/docs/guides/filter-your-data.md)
- [/docs/guides/build-a-custom-dashboard.md](https://www.mux.com/docs/guides/build-a-custom-dashboard.md)
- [/docs/guides/save-and-share-filter-sets.md](https://www.mux.com/docs/guides/save-and-share-filter-sets.md)
- [/docs/guides/error-categorization.md](https://www.mux.com/docs/guides/error-categorization.md)
- [/docs/guides/export-raw-video-view-data.md](https://www.mux.com/docs/guides/export-raw-video-view-data.md)
- [/docs/guides/export-amazon-kinesis-data-streams.md](https://www.mux.com/docs/guides/export-amazon-kinesis-data-streams.md)
- [/docs/guides/export-google-cloud-pubsub.md](https://www.mux.com/docs/guides/export-google-cloud-pubsub.md)
- [/docs/guides/setup-alerts.md](https://www.mux.com/docs/guides/setup-alerts.md)
- [/docs/guides/pagerduty-alert-notifications.md](https://www.mux.com/docs/guides/pagerduty-alert-notifications.md)
- [/docs/guides/enable-automatic-cdn-detection.md](https://www.mux.com/docs/guides/enable-automatic-cdn-detection.md)
- [/docs/guides/engagement-hotspots-and-heatmaps.md](https://www.mux.com/docs/guides/engagement-hotspots-and-heatmaps.md)
- [/docs/guides/see-how-many-people-are-watching.md](https://www.mux.com/docs/guides/see-how-many-people-are-watching.md)
- [/docs/guides/build-a-custom-data-integration.md](https://www.mux.com/docs/guides/build-a-custom-data-integration.md)
- [/docs/guides/data-custom-javascript-integration.md](https://www.mux.com/docs/guides/data-custom-javascript-integration.md)
- [/docs/guides/data-custom-swift-integration.md](https://www.mux.com/docs/guides/data-custom-swift-integration.md)
- [/docs/guides/data-custom-java-integration.md](https://www.mux.com/docs/guides/data-custom-java-integration.md)
- [/docs/guides/mux-data-playback-events.md](https://www.mux.com/docs/guides/mux-data-playback-events.md)
- [/docs/guides/export-monitoring-data.md](https://www.mux.com/docs/guides/export-monitoring-data.md)
- [/docs/guides/ensure-data-privacy-compliance.md](https://www.mux.com/docs/guides/ensure-data-privacy-compliance.md)
- [/docs/guides/integrate-a-data-custom-domain.md](https://www.mux.com/docs/guides/integrate-a-data-custom-domain.md)
- [/docs/guides/track-autoplaying-videos.md](https://www.mux.com/docs/guides/track-autoplaying-videos.md)
- [/docs/guides/mux-data-faqs.md](https://www.mux.com/docs/guides/mux-data-faqs.md)
- [/docs/guides/signing-jwts.md](https://www.mux.com/docs/guides/signing-jwts.md)
- [/docs/guides/secure-video-playback.md](https://www.mux.com/docs/guides/secure-video-playback.md)
- [/docs/guides/protect-videos-with-drm.md](https://www.mux.com/docs/guides/protect-videos-with-drm.md)
- [/docs/guides/play-drm-protected-videos-on-google-cast.md](https://www.mux.com/docs/guides/play-drm-protected-videos-on-google-cast.md)
- [/docs/guides/dashboard-environment-restrictions.md](https://www.mux.com/docs/guides/dashboard-environment-restrictions.md)
- [/docs/integrations/mcp-server.md](https://www.mux.com/docs/integrations/mcp-server.md)
- [/docs/integrations/installing-mcp-server-locally.md](https://www.mux.com/docs/integrations/installing-mcp-server-locally.md)
- [/docs/integrations/mux-cli.md](https://www.mux.com/docs/integrations/mux-cli.md)
- [/docs/integrations/mux-node-sdk.md](https://www.mux.com/docs/integrations/mux-node-sdk.md)
- [/docs/integrations/mux-python-sdk.md](https://www.mux.com/docs/integrations/mux-python-sdk.md)
- [/docs/integrations/mux-php-sdk.md](https://www.mux.com/docs/integrations/mux-php-sdk.md)
- [/docs/integrations/mux-ruby-sdk.md](https://www.mux.com/docs/integrations/mux-ruby-sdk.md)
- [/docs/integrations/mux-elixir-sdk.md](https://www.mux.com/docs/integrations/mux-elixir-sdk.md)
- [/docs/integrations/mux-java-sdk.md](https://www.mux.com/docs/integrations/mux-java-sdk.md)
- [/docs/integrations/mux-csharp-sdk.md](https://www.mux.com/docs/integrations/mux-csharp-sdk.md)
- [/docs/integrations/cms.md](https://www.mux.com/docs/integrations/cms.md)
- [/docs/integrations/sanity.md](https://www.mux.com/docs/integrations/sanity.md)
- [/docs/integrations/contentful.md](https://www.mux.com/docs/integrations/contentful.md)
- [/docs/integrations/wordpress.md](https://www.mux.com/docs/integrations/wordpress.md)
- [/docs/integrations/strapi.md](https://www.mux.com/docs/integrations/strapi.md)
- [/docs/integrations/cosmic.md](https://www.mux.com/docs/integrations/cosmic.md)
- [/docs/integrations/datocms.md](https://www.mux.com/docs/integrations/datocms.md)
- [/docs/integrations/prepr.md](https://www.mux.com/docs/integrations/prepr.md)
- [/docs/integrations/database-schema.md](https://www.mux.com/docs/integrations/database-schema.md)
- [/docs/integrations/supabase.md](https://www.mux.com/docs/integrations/supabase.md)
- [/docs/integrations/convex.md](https://www.mux.com/docs/integrations/convex.md)
- [/docs/pricing/overview.md](https://www.mux.com/docs/pricing/overview.md)
- [/docs/pricing/report-on-mux-costs.md](https://www.mux.com/docs/pricing/report-on-mux-costs.md)
- [/docs/pricing/estimating-video-costs.md](https://www.mux.com/docs/pricing/estimating-video-costs.md)
- [/docs/pricing/optimizing-video-costs.md](https://www.mux.com/docs/pricing/optimizing-video-costs.md)
- [/docs/pricing/export-usage-data-as-a-csv.md](https://www.mux.com/docs/pricing/export-usage-data-as-a-csv.md)
- [/docs/examples/moderate-video-content.md](https://www.mux.com/docs/examples/moderate-video-content.md)
- [/docs/examples/synchronize-video-playback.md](https://www.mux.com/docs/examples/synchronize-video-playback.md)
- [/docs/examples/use-videos-in-your-website-design.md](https://www.mux.com/docs/examples/use-videos-in-your-website-design.md)