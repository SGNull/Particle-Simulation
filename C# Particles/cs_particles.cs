using System;

namespace CSharpParticles{
    class Particle{
        public int[,] Position {get; set;}
        public int[,] Velocity {get; set;}
        public int Color {get; set;}
        public Particle(int xPos, int yPos, int color){
            Velocity = new int{0,0};
            Position = new int{xPos, yPos};
            Color = color;
        }
    }
    class Vector2Math{
        public int[,] ScalMult(int[,] vect, int scal) {
            int[,] newVect = new int[2];
            newVect[0] = vect[0] * scal;
            newVect[1] = vect[1] * scal;
        }
        public int[,] Normalize(int[,] vect){
            
        }
    }
    class Program{
        int numParticles = 201;
        int numColors = 3;
        int particleRadius = 5;
        int contactRadius = 6;

        Particle[] Universe = new Particle[numParticles];

        static void Main(string[] args){
            running = false;
            while (running){

            }
        }
        static void initUniverse(){

        }

        static void bakeUniversePie(){

        }
    }
}