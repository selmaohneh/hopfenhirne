using System.Text.Unicode;
using Google.Apis.Services;

namespace hopfenhirne;


public class GoogleSheetsService
{
  public async Task<IEnumerable<Member>> GetMembers()
  {
      var initializer = new BaseClientService.Initializer
      {
          ApplicationName = "hopfenhirne",
          GZipEnabled = false,
          ApiKey = System.Text.Encoding.UTF8.GetString(System.Convert.FromBase64String("QUl6YVN5QXJtbGxNdUx3MUhHaFdwLVhhZG9Oc2o3UWhHMndIcjVR"))
      };
            
      var service = new Google.Apis.Sheets.v4.SheetsService(initializer);
                
      var result = await service.Spreadsheets.Values.Get("1-FmJ9lWEBgSp_JKDoCLgXaCGqb_n1iCB0iYvTpFvFTI", "A9:H36").ExecuteAsync();

      var members = new List<Member>();
      foreach (var row in result.Values)
      {
          var name = (string)row[0];
          var number = Convert.ToInt32(row[1]);
          var numberOfParticipations = Convert.ToInt32(row[2]);
          var numberOfQuizParticipations =Convert.ToInt32( row[3]);
          var numberOfQuizWins = Convert.ToInt32(row[4]);
          var numberOfQuizHostings =Convert.ToInt32(row[7]);
          var member = new Member(name, number, numberOfParticipations, numberOfQuizParticipations, numberOfQuizWins,
              numberOfQuizHostings);

          if (!string.IsNullOrWhiteSpace(member.Name) && member.NumberOfParticipations > 1)
          {
              members.Add(member);
          }
      }

      return members;
  }
}
