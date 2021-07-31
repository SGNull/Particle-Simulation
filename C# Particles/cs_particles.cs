using System;
using Math;

namespace CSharpParticles{
    class Particle{
        public double[] Position {get; set;}
        public double[] Velocity {get; set;}
        public int Color {get; set;}
        public Particle(double xPos, double yPos, int color){
            Velocity = new double{0,0};
            Position = new double{xPos, yPos};
            Color = color;
        }
        public Draw(){

        }
        public UpdatePosition(){

        }
    }
    class Vector2Math{
        public double[] ScalMult(double[] vect, double scal) {
            double[] newVect = new double[2];
            newVect[0] = vect[0] * scal;
            newVect[1] = vect[1] * scal;
            return newVect;
        }
        public double[] Normalize(double[] vect){
            double[] newVect = new double[2];
            double magnitude = Magnitude(vect);
            newVect[0] = vect[0]/magnitude;
            newVect[1] = vect[1]/magnitude;
            return newVect;
        }
        public double Magnitude(double[] vect){
            return Math.Pow(vect[0]*vect[0] + vect[1]*vect[1], 0.5);
        }
        public double[] Modulo(double[] vect, double mod){
            double[] newVect = new double[2];
            newVect[0] = vect[0] % mod;
            newVect[1] = vect[1] % mod;
            return newVect;
        }
        public double[] MakeDistanceVect(double[] vect1, double[] vect2){
            double[] newVect = new double[2];
            newVect[0] = vect2[0] - vect1[0];
            newVect[1] = vect2[1] - vect1[1];
            return newVect;
        }
    }
    class Program{
        int numParticles = 201;
        int numColors = 3;
        double particleRadius = 5;
        double contactRadius = 6;

        Particle[] Universe = new Particle[numParticles];
        int numSlices = (numParticles*(numParticles-1))/2;
        Particle[,] UniversePie = new Particle[numSlices,2];

        static void Main(string[] args){
            InitUniverse();
            BakeUniversePie();
            running = false;
            while (running){
                PhysStep();
                DrawScreen();
            }
        }
        static void InitUniverse(){

        }

        static void BakeUniversePie(){

        }
        static void PhysStep(){

        }
        static void SimulateSlice(Particle[,] sliceOfPie){

        }
        static void DrawScreen(){
            
        }
    }
}