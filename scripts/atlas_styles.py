"""Port the actual original's visual rules into the shared profile namespace."""
import re
def build_styles(root,out):
 original=(root/'dist/style.css').read_text(encoding='utf8')
 mapping={
 'header':'p-header','brand':'p-brand','highlights-link':'p-highlight-link','menu-toggle':'p-menu-trigger',
 'contours':'p-contours','hero-shell':'p-hero-shell','hero':'p-hero','hero-viewport':'p-frame','hero-contours':'p-hero-contours','hero-tools':'p-hero-tools','hero-marquee':'p-marquee','portrait-caption':'p-portrait-caption','champion-badge':'p-team-badge','scroll-cue':'p-scroll-cue',
 'faceoff':'p-dual','faceoff-portrait':'p-dual-portrait','faceoff-jett':'p-dual-agent','faceoff-kk':'p-dual-player','faceoff-links':'p-dual-copy','faceoff-labels':'p-dual-label',
 'manifesto':'p-manifesto','moments':'p-photo-section','moments-stage':'p-photo-stage','gallery-caption':'p-photo-title','gallery-window':'p-photo-window','gallery':'p-photo-track','shot':'p-shot','photo-quote':'p-photo-quote','gallery-bottom':'p-photo-controls',
 'agents':'p-agent-section','agent-intro':'p-section-title','agent-cards':'p-agent-cards','agent-card':'p-agent-card','agent-letter':'p-agent-letter','agent-card-label':'p-agent-label','agent-hover':'p-agent-explore','agent-details':'p-agent-detail','metric':'p-agent-metric','data-note':'p-data-note',
 'champion':'p-feature','champion-image':'p-feature-frame','watch':'p-next',
 }
 # Existing result rows and dialogs keep their already validated responsive structure.
 retained=[(root/'scripts/profile-structure.css').read_text(encoding='utf8')]
 converted=re.sub(r'\.([A-Za-z][\w-]*)',lambda m:'.'+mapping.get(m[1],m[1]),original)
 converted=converted.replace('#hero-reveal','.p-canvas')
 # Do not inherit original root footer selectors or unused body-wide dialog positioning.
 converted=re.sub(r'(?<![.\w-])footer\b','.p-unused-footer',converted)
 base="@import url('../assets/manrope.css');\n"
 adapters=(root/'scripts/profile-layout.css').read_text(encoding='utf8')
 (out/'profile.css').write_text(base+converted+'\n'+'\n'.join(retained)+'\n'+adapters,encoding='utf8')
