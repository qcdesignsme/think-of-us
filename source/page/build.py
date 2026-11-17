import json, base64, sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
P=lambda *a: os.path.join(*a)
MC = "https://qcdesigns.me/p/022d282b"
PROTO = sys.argv[1] if len(sys.argv)>1 else "prototype/"
needs = [
 {"name":"Service design and journey mapping","listPill":"Strong","panelPill":"Strong match",
  "title":"I map the full service, including what happens when it fails",
  "buttons":[{"label":"Full case study","href":MC}],
  "quote":"Map the end-to-end experience, not just the screens.",
  "why":[["Mentor Collective","Using data from 100+ participants over 14 studies, I mapped first-time journeys for mentors and mentees from recruitment to program end. I covered thinking, feeling, pain points, touchpoints, and improvements."],
         ["Mentor Collective","Point of failure: My analysis uncovered a widespread ghosting issue, so I created two more journeys for the ghosted mentor and the ghosting mentee."],
         ["Mentor Collective","Designed learning across three portals: the admin tool- for staff to set up mentor programs, the participant portal - for mentors and mentees to connect, and the partner dashboard - for institutions to track mentorship progress."]],
  "images":[{"src":"img/journeys.jpg","crop":290,"pos":"50% 18%","alt":"The first-year mentorship journey map for mentors and mentees, with a section on what happens when a relationship goes quiet","cap":"Journey maps built from 14 studies (~100 participants). Click to enlarge."}]},
 {"name":"Research with people under stress","listPill":"Strong","panelPill":"Strong match",
  "title":"I've planned and run trauma-informed research",
  "quote":"Bring sound judgment and genuine empathy to designing for people navigating stress and crisis.",
  "why":[["VA.gov","Co-ran concept testing of the VA mental health claim form with 9 Veterans whose claims included combat, military sexual trauma, and other events."],
         ["VA.gov","Built in safeguards: screening calls that named the sensitive topics, optional recordings, optional breaks in 90-minute sessions, few observers, and warnings before hard content."],
         ["VA.gov","Surfaced a finding that changed the design: 7 of 9 Veterans couldn't imagine skipping a section and still getting a fair rating. Optional rarely feels optional."]],
  "template":"flow0781"},
 {"name":"Interaction design for staff tools","listPill":"Strong","panelPill":"Strong match",
  "title":"I redesign the tools staff depend on, and test them with staff",
  "buttons":[{"label":"Full case study","href":MC},{"label":"Interactive Prototype","href":PROTO}],
  "quote":"A CR workbench that amplifies what a good responder can do.",
  "why":[["Mentor Collective","Program managers worked in a legacy tool with 50%+ error rates when creating programs for participants."],
         ["Mentor Collective","Four rounds of testing with 8 program managers showed they reuse tasks rather than create them. I rebuilt the flow library-first: find, review, adjust, confirm."]],
  "embed":{"src":PROTO,"title":"Interactive prototype: Mentor Collective Add Task(s) flow, sample data","poster":"img/admin-flow.jpg","posterAlt":"Redesigned Add Task(s) flow: search, filters, a task table and a Selected Tasks panel","cap":"After: a library-first flow with clear steps and inline guidance. Try it here (sample data)."}},
 {"name":"Legible AI and human-in-the-loop","listPill":"In-progress","panelPill":"Partial match","partial":True,
  "title":"I've designed for informed choice. I haven't yet shipped AI-facing UI.",
  "quote":"Design for uncertainty: help-seekers and CRs need to understand what the AI is doing and why, and be able to override it.",
  "why":[["VA.gov","Designed decision points people can reverse: an informed-choice page, confirmation before deleting, and opt-outs at review. 8 of 9 Veterans understood their options."],
         ["VA.gov","Teammates credited me for diving into Copilot and developer tools to improve data."]],
  "template":"concept"},
 {"name":"Design systems and quality","listPill":"Strong","panelPill":"Strong match",
  "title":"Through user research, I evolve pattern libraries into design systems.",
  "buttons":[{"label":"VA Design System","href":"https://design.va.gov/"}],
  "quote":"Establish and maintain a design system and component standards across both modules and multiple state deployments.",
  "why":[["farmers.gov","Usability-tested the design system with 6 designers from 4 teams: 98% task completion and 6 recommendations, from navigation to a change log."],
         ["VA.gov","Tested VA multi-response patterns with Veterans and documented where each one breaks. Worked with accessibility staff to ensure the pattern was reusable across VA."]],
  "images":[{"src":"img/handoff.jpg","crop":430,"alt":"Required multi-page pattern user flow: introduction, questions, cancel, summary, edit and delete flows","cap":"Mentor Collective hand-off: the participant side of the system."}]},
 {"name":"Alignment through influence","listPill":"Strong","panelPill":"Strong match",
  "title":"I get engineering, product, and program partners to one direction",
  "buttons":[{"label":"Full case study","href":MC}],
  "quote":"Move cross-functional work forward through influence rather than authority.",
  "why":[["Mentor Collective","Re-designed processes adopt by all 3 team including engineers, a product manager, a content designer, and a learning lead on one product vision."],
         ["VA.gov","Drove the research plan, conversation guide, prototype, and timeline for the Copy of Submission study through changing circumstances."]],
  "images":[{"src":"img/workflow.jpg","alt":"Team Nala new process in four stages: discovery and research, team spikes the roadmap, design and developer estimation, build","cap":"Created a new workflow for all teams"}]},
]
t = open(P(HERE,'template.html')).read()
t = t.replace('{{STAGE}}', open(P(HERE,'stage.html')).read())
t = t.replace('{{VA_DECK}}', '#work').replace('{{VA_DECK_ATTR}}', ' aria-disabled="true" title="Link to be added"')
logos = json.load(open(P(HERE,'..','animation','logos.json')))
t = t.replace('{{LOGOS}}', json.dumps(logos))
t = t.replace('{{NEEDS}}', json.dumps(needs, ensure_ascii=False).replace('</', '<\\/'))
open(P(ROOT,'index.html'),'w').write(t)
# self-contained build: inline the images
s = t.replace('"src": "prototype/"','"src": "https://qcdesignsme.github.io/think-of-us/prototype/"').replace('"href": "prototype/"','"href": "https://qcdesignsme.github.io/think-of-us/prototype/"')
for name in ['journeys','admin-flow','handoff','workflow']:
    b = base64.b64encode(open(P(ROOT,'img',f'{name}.jpg'),'rb').read()).decode()
    s = s.replace(f'img/{name}.jpg', 'data:image/jpeg;base64,'+b)
open(P(HERE,'qian-chen-think-of-us.html'),'w').write(s)
print(len(t)//1024, 'KB index;', len(s)//1024, 'KB self-contained')
