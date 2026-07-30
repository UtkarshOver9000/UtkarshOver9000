<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=26&duration=3000&pause=800&color=8B5E3C&center=true&vCenter=true&width=600&lines=Hey%2C+I'm+Utkarsh+%F0%9F%A6%A5;MLOps+%2B+Security+ML+%2B+AI+Systems;I+build+slow%2C+deliberate%2C+very+solid+things;Currently+debugging+something+at+2am" alt="Typing SVG" />

</div>

---

### 🦥 About Me

I move like a sloth, ship like it too — slow, deliberate, hard to knock off the branch.
I work across **MLOps**, **security ML**, and general **AI systems** — the stuff that has to actually run in production, not just work in a notebook.

- 🔐 Interested in ML for security: anomaly detection, auth/fraud signals, threat modeling
- ⚙️ Into MLOps: pipelines, deployment, monitoring, making models survive contact with reality
- 🧠 Generally curious about AI systems end-to-end — not just models, the whole stack around them
- 🛠️ I build weird, sometimes overbuilt things because "why not"

---

### 🧰 Tech Stack

<div align="center">
<img src="https://skillicons.dev/icons?i=python,pytorch,tensorflow,docker,kubernetes,git,linux,fastapi,postgres,aws,githubactions,bash&perline=6" />
</div>

---

### 📊 GitHub Stats

<div align="center">

<img src="https://github-readme-stats.vercel.app/api?username=UtkarshOver9000&show_icons=true&theme=algolia&hide_border=true&count_private=true" height="165"/>
<img src="https://github-readme-streak-stats.herokuapp.com/?user=UtkarshOver9000&theme=algolia&hide_border=true" height="165"/>

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=UtkarshOver9000&layout=compact&theme=algolia&hide_border=true" height="165"/>

</div>

---

### 🦥 Contribution Graph — Sloth Mode

<div align="center">

<!-- This uses the Platane/snk action but recolored to a mossy sloth palette instead of the default snake colors -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/UtkarshOver9000/UtkarshOver9000/output/github-sloth-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/UtkarshOver9000/UtkarshOver9000/output/github-sloth.svg" />
  <img alt="sloth eating contributions" src="https://raw.githubusercontent.com/UtkarshOver9000/UtkarshOver9000/output/github-sloth.svg" />
</picture>

*(one contribution eaten per nap — see setup note below)*

</div>

---

### 📫 Reach Me

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/utkarsh-sharma-lm10)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:utkarshs123op@gmail.com)

</div>

<div align="center">
<img src="https://komarev.com/ghpvc/?username=UtkarshOver9000&label=Profile+Views&color=8B5E3C&style=flat" />
</div>

---

<!--
SETUP NOTES:

1. Create a repo named exactly "UtkarshOver9000" (must match your username) if you don't have one yet.
   Put this file in it as README.md — it auto-renders on your profile page.

2. Typing header / stats / streak / top-langs / visitor counter all work immediately,
   no setup needed — they're hosted services pulling live from your GitHub username.

3. For the "sloth mode" contribution graph:
   - This is really the Platane/snk action, just recolored (browns/mossy greens instead of green/snake colors)
   - It needs a GitHub Action to generate it. Add this file as
     .github/workflows/sloth.yml in your UtkarshOver9000 repo:

     name: generate sloth graph
     on:
       schedule:
         - cron: "0 */12 * * *"
       workflow_dispatch:
       push:
         branches: [main]
     jobs:
       build:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v4
           - uses: Platane/snk/svg-only@v3
             with:
               github_user_name: ${{ github.repository_owner }}
               outputs: |
                 dist/github-sloth.svg?color_snake=%238B5E3C&color_dots=#e8dcd0,#c9b8a3,#a68b6f,#8b6f4e,#6b4f2e
                 dist/github-sloth-dark.svg?palette=github-dark&color_snake=%23c9a679
           - uses: crazy-max/ghaction-github-pages@v3
             with:
               target_branch: output
               build_dir: dist
             env:
               GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

   - Enable Actions in repo Settings if prompted, then run it once manually
     (Actions tab -> the workflow -> "Run workflow") so the "output" branch exists.
   - The image URLs in this README already point at the right paths once that's live.

4. Swap the LinkedIn/Email badge links (the "#") for your real profile + mailto link.
-->
