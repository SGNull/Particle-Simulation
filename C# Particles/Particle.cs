namespace CSharpParticles{
    public partial class Particle{
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
}