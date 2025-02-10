using System.Globalization;

namespace hopfenhirne;

public record Member(
    string Name,
    int Number,
    int NumberOfParticipations,
    int NumberOfQuizParticipations,
    int NumberOfQuizWins,
    int NumberOfQuizHostings)
{
    public double WinRate
    {
        get
        {
            if (NumberOfQuizParticipations < 3)
            {
                return Double.NaN;
            }
            
            return 100 * NumberOfQuizWins / (double)NumberOfParticipations;
        }
    }
    
    public string WinRatePlot()
    {
        if (double.IsNaN(WinRate))
        {
            return "-";
        }

        return Math.Round(WinRate, 1).ToString(CultureInfo.InvariantCulture);

    }
}