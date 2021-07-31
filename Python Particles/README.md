# Python-Particles
This is a small project I'm currently working on to familiarize myself with programming again. A while ago I got really interested in Code Parade's Particle Life simulation here: https://www.youtube.com/watch?v=Z_zmZ23grXE. I tried making my own version of it but it didn't turn out properly, so I thought coming back to this would be good to get back into coding

I chose python because it's fairly easy to work with, much easier than I had realized. I've never made any sort of project in it though, so it will be nice to properly learn a new language.

Particles have their own class, and are stored in the "Universe" list. Each particle has a color, which determines its interaction with other particles. These interactions are stored in a full matrix. This isn't a triangular matrix, because we don't care about thermodynamics. Having only symmetric interactions would result in a "heat-death" fairly quickly, and would be really uninteresting. Instead, the full matrix means that particles can chase each-other around, resulting in a net-increase in energy in the system.
