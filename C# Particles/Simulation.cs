using System;
using System.Drawing;
using System.Windows.Forms;
using Math;

namespace CSharpParticles{
    
    class Program{
        int numParticles = 201;
        int numColors = 3;
        double particleRadius = 5;
        double contactRadius = 6;
        double minForceDist = 50;
        double maxForceDist = 150;

        Particle[] Universe = new Particle[numParticles];
        int numSlices = (numParticles*(numParticles-1))/2;
        Particle[,] UniversePie = new Particle[numSlices,2];
        double[,,] InteractionsMatrix = new double[numColors,numColors,3];

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