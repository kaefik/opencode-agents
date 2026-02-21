# 1. Install Superpowers (or update existing)
if [ -d .opencode/superpowers ]; then
  cd .opencode/superpowers && git pull
else
  git clone https://github.com/obra/superpowers.git .opencode/superpowers
fi

# 2. Create directories
mkdir -p .opencode/plugins .opencode/skills

# 3. Remove old symlinks/directories if they exist
rm -f .opencode/plugins/superpowers.js
rm -rf .opencode/skills/superpowers

# 4. Create symlinks
ln -sf ../superpowers/.opencode/plugins/superpowers.js .opencode/plugins/superpowers.js
ln -sf ../superpowers/skills .opencode/skills/superpowers

# 5. Restart OpenCode



