# Author: Drew Tweedale
# Last modified: April 27 2024
# Group 5

"""
This file is a config file for the preloaded sample notes for Chapter 2 of Sommerville"s textbook. It contains
three string representations of dictionaries and a note_name that are parsed by note_storage.py when creating the
"Admin" user. We"ve seperated this from the note_storage.py module since the raw text is quite ugly, and 
distracts from the storage code.
"""

note_name = "Chapter 2: Software Processes"

headers= ("{'0': '2.1 Software Process Models', '1': '2.1.1 The Waterfall Method', '2':"+
           "'2.1.2 Incremental Development', '3': '2.1.3 Integration and Configuration',"+
            "'4': '2.2 Process Activities', '5': '2.2.1 Software Specification', '6': '2."+
            "2.2 Software Design and Implementation', '7': '2.2.3 Software Validation', '8':"+
             " '2.2.4 Software Evolution', '9': '2.3 Coping with Change', '10': '2.3.1 Prototyping',"+
              " '11': '2.3.2 Incremental Delivery', '12': '2.4 Process Improvement'}")

notes= ("{'2': 'Based on the idea of developing an initial implementation, getting feedback, and evolving"+
        " the software through several versions until requirements are met .Specification, development, and "+
        "validation are interleaved .Most common approach for applications systems and software products .Better"+
         " than waterfall for systems whose requirements are likely to change during development .Each new"+
          " increment/version incorporates a functionality needed by customer .3 major advantages: Reduced cost for"+
           " implementing requirement changes, Easily get customer feedback on work that has been done,"+
            " Early delivery of useful software, even if not all functionality present . 2 problems in managemen"+
            "t perspective: Process not visible, System structure tends to degrade as new increments added."+
             " Not good for large, complex, long-term systems where different parts are developed by different"+
              " teams. Not all increments must be delivered to customer', '6': 'Implementation: process of"+
               " developing an executable system for delivery to customers. Design: description of structure"+
                " of software to be implemented. Design includes data models and structures, interfaces"+
                 " between components and sometimes algorithms used. Design & Implementation: transfo"+
                 "rming required specification into an executable . Figure 2.5 Abstract model of design"+
                  " process: shows inputs, design activities, outputs. 4 main design activities:"+
                   " architectural, database, interface, component selection. Development of a program to implement"+
                    " a system flows naturally from design. Testing establishes the existence of defects .Debugging"+
                     " is concerned with locating and correcting defects', '8': 'Flexibility is the main"+
                      " reason more software is reused. Development and maintenance used to be split, combined "+
        "as evolution. Evolution: change existing systems to meet new requirements. Figure 2.8 Software system"+
        " evolution: software continually changed over its lifetime in response to changes in requirement or"+
        " customer needs', '12': 'Process Improvement: to enhance existing software processes to better software"+
        " quality, lower the development cost and time. Two approaches: process maturity, agile. Figure 2.11 "+
        "general improvement cycle process. Cyclic process involving measurement, analysis, and change. Figure"+
        " 2.12 Capability maturity levels process. Levels: initial, managed, defined, quantitatively managed,"+
         " optimizing'}")


bullets= ("{'0': '● a simplified representation of a software process\n● Generic models: high-level,"+
        " abstract descriptions of software processes that can be used to explain different approaches"+
        " to software development\n● Generic models: describes the organization of software processes\n● Ge"+
        "neric Process Models Examples: Waterfall model, Incremental development, Integration and configur"+
        "ation\n● No universal process model is right for all kinds of software development\n● Lots of practi"+
        "cal software processes based on general models but incorporate features of other models\n', '1':"+
         " '● Presents software development process as a number of stages that cascade from one phas"+
         "e to another\n● Plan-driven process\n● Stages directly reflect fundamental software developmen"+
         "t activities: Requirements analysis and definition, System and Software design, Implementatio"+
         "n and Unit testing, Integration and system testing, Operation and maintenance\n● Result of eac"+
         "h phases is one or more documents that are approved\n● Following phases should not start until previ"+
         "ous has finished\n', '3': '● Majority of software projects have some software reuse\n● 3 type"+
         "s of components frequently reused: Stand-alone application systems , Collections of objects, We"+
         "b services\n● Figure 2.3 general process model for reuse-based development based on integration an"+
         "d configuration\n● Stages: requirement specification, software discovery and evaluation, requireme"+
         "nts refinement, application system configuration, component adaptation and interrogation\n● Advantag"+
         "es: reduces amount of software to be developed, cost, risk, and time\n', '4': '● Real softwar"+
         "e processes\n● Interleaved sequences of technical, collaborative, and managerial activities\n● Ov"+
         "erall goal: to specify, design, implement and test software systems\n● Four basic process activitie"+
         "s: specification, development, validation, evolution\n● Organized differently in different developme"+
         "nt processes: depends on type of software, experience of developers, and type of organizati"+
         "on\n', '5': '● Process of defining what services are necessary from the system and identifyin"+
         "g the constraints on the operation and development\n● Requirements engineering: the process of devel"+
         "oping a software specification\n● Figure 2.4 Requirements Engineering process: aims to produce an a"+
         "greed requirements document that specifies a system satisfying stakeholder requirements\n● Presente"+
         "d at 2 levels of details: End-users need high level, developers need more details\n● 3 main activitie"+
         "s: requirement elicitation and analysis, requirement specification, requirement validation\n● Activiti"+
         "es of analysis, definition, and specification are interleaved\n● Activities of analysis, definitio"+
         "n, and specification are interleaved\n● In agile methods: specification not a separate activity bu"+
         "t part of system development\n', '7': '● More generally: verification and validation (V & V)\n● Intend"+
         "ed to show that a system specification and expectation of users are met\n● Figure 2.6 three-stage testi"+
         "ng process: System components are individually tested, then integrated system tested\n● Stages in test"+
         "ing process: components testing, system testing, customer testing\n● Ideally: component defects foun"+
         "d early, interface problems found when integrated\n● Incremental approach: each increment tested a"+
         "s developed\n● Plan-driven process: testing driven by set of test plans\n● Figure 2.7 (V-mode"+
         "l) illustrates how test plans are linked between testing and development activities\n● Beta test"+
         "ing: testing process for software products\n', '9': '● Change is inevitable in large project"+
         "s\n● In an model, needs to be able to accommodate change\n● Rework: work that has been complete"+
         "d has to be redone\n● Two approaches to reduce cost of rework: change anticipation, change toler"+
         "ance\n● Two ways to cope with change and change of system requirements: system prototyping, increm"+
         "ental delivery\n', '10': '● Early version of system used to demonstrate concepts, try out design opti"+
         "ons, find more about the problem and possible solutions\n● Helps avoid poor decisions on requiremen"+
         "ts and design\n● Allows for design experimentation checking feasibility of design\n● Figure 2.9 Prototyp"+
         "e development process model\n● First stage: make objective of a prototype explicit\n● Next stage: d"+
         "ecide what to put in and leave out\n● Final stage: evaluate the prototype\n', '11': '● An approach to de"+
         "velopment where increments are delivered to customer and deployed for use in their working environme"+
         "nt\n● Figure 2.10 incremental delivery model\n● Increments are integrated when completed, impr"+
         "oving functionality\n● Changes can be made without disrupting system as whole\n● Advantages: cust"+
         "omer feedback, early delivery of some functionality, easy to incorporate change, highest priorit"+
         "y services receive most testing (done first)\n● Problems: replacing old system difficult, har"+
         "d to identify common facilities, no complete specification until final increment specified\n'}")
