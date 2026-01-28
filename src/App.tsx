import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { TrendingUp, Instagram, Music, Mail, Link2 } from 'lucide-react'

// Links data - edit labels/urls here
const LINKS = [
  // Replaced the old personal website link with CatalogLAB™ demo as requested
  { id: 'cataloglab', label: 'CatalogLAB™', href: 'https://lab.perdaycatalog.com', icon: 'graph' },
  { id: 'instagram', label: 'Instagram', href: 'https://www.instagram.com/iamjsmash', icon: 'instagram' },
  // Kept the music entry but swapped to a new icon (vinyl) for a clearer music visual
  { id: 'music', label: 'My Music', href: 'https://tidal.com/browse/album/228219175?u', icon: 'vinyl' },
  { id: 'work', label: "Let's Work", href: 'https://tally.so/r/wokZYP', icon: 'mail' }
]

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.06 } }
}

const itemVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 360, damping: 28 } }
}

function Icon({ name }: { name: string }) {
  switch (name) {
    case 'instagram':
      return <Instagram size={18} />
    case 'music':
    case 'vinyl':
      return <Music size={18} />
    case 'mail':
      return <Mail size={18} />
    case 'graph':
    case 'catalog':
    case 'cataloglab':
      return <TrendingUp size={18} />
    default:
      return <Link2 size={18} />
  }
}

export default function App(): JSX.Element {
  return (
    <div className="page-root">
      <main className="card" role="main">
        <header className="profile">
          <div className="avatar-wrap" aria-hidden>
            {/* Animated gradient ring (SVG) behind the avatar */}
            <svg className="avatar-ring" viewBox="0 0 200 200" preserveAspectRatio="xMidYMid meet" aria-hidden>
              <defs>
                <linearGradient id="g1" x1="0%" x2="100%">
                  <stop offset="0%" stopColor="#7c3aed" />
                  <stop offset="50%" stopColor="#8b5cf6" />
                  <stop offset="100%" stopColor="#ff7a59" />
                </linearGradient>
              </defs>
              <g transform="translate(100,100)">
                <circle r="78" stroke="url(#g1)" strokeWidth="6" strokeLinecap="round" strokeDasharray="6 8" fill="none" opacity="0.95" />
                <circle r="88" stroke="url(#g1)" strokeWidth="2" strokeLinecap="round" strokeDasharray="2 6" fill="none" opacity="0.45" />
              </g>
            </svg>

            <img
              className="avatar"
              src="https://content.app-sources.com/s/98880833099935832/uploads/Images/Untitled-1029430.png?format=webp"
              alt="J Smash"
              width={160}
              height={160}
            />
          </div>

          <h1 className="title">J Smash of The Nukez</h1>
          <p className="subtitle">Grammy‑nominated producer • Rap · RnB · Pop</p>
        </header>

        <AnimatePresence>
          <motion.nav
            className="links"
            initial="hidden"
            animate="visible"
            variants={containerVariants}
            aria-label="Primary Links"
          >
            {LINKS.map((l) => (
              <motion.a
                key={l.id}
                href={l.href}
                target="_blank"
                rel="noopener noreferrer"
                className="link"
                variants={itemVariants}
                whileHover={{ y: -6, boxShadow: '0 20px 40px rgba(12,18,40,0.5)' }}
                whileTap={{ scale: 0.98 }}
                aria-label={l.label}
              >
                <span className="icon-circle">
                  <span className="icon-inner">
                    <Icon name={l.icon} />
                  </span>
                </span>
                <span className="label">{l.label}</span>
              </motion.a>
            ))}
          </motion.nav>
        </AnimatePresence>

        <footer className="footer">Made with care — <a href="https://smashhouserecordings.com">Smash House</a></footer>
      </main>
    </div>
  )
}
