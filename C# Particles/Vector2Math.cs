namespace CSharpParticles{
    public partial class Vector2Math{
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
}