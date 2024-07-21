using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace SteamTopSellers
{
    class Program
    {
        private static readonly HttpClient client = new HttpClient();

        private const string url = "https://store.steampowered.com/api/featuredcategories/";

        public class Game
        {
            public int rank { get; set; }
            public string name { get; set; }
            public string price_final_formatted { get; set; }
        }

        public class FeaturedGamesResponse
        {
            public List<Game> bestseller { get; set; }
        }

        static async Task Main(string[] args)
        {
            try
            {
                var games = await GetTopSellersAsync();
                DisplayTopSellers(games);
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"Ошибка запроса: {e.Message}");
            }
            catch (JsonException e)
            {
                Console.WriteLine($"Ошибка обработки данных: {e.Message}");
            }
            catch (Exception e)
            {
                Console.WriteLine($"Произошла ошибка: {e.Message}");
            }

            Console.WriteLine("Нажмите любую клавишу для выхода...");
            Console.ReadKey();
        }

        private static async Task<List<Game>> GetTopSellersAsync()
        {
            var response = await client.GetStringAsync(url);
            var featuredGames = JsonConvert.DeserializeObject<FeaturedGamesResponse>(response);
            return featuredGames.bestseller?.GetRange(0, Math.Min(10, featuredGames.bestseller.Count));
        }

        private static void DisplayTopSellers(List<Game> games)
        {
            Console.WriteLine("Топ-10 лидеров продаж в Steam (РФ):");
            Console.WriteLine("------------------------------------");

            if (games != null && games.Count > 0)
            {
                foreach (var game in games)
                {
                    Console.WriteLine($"{game.rank}. {game.name} - {game.price_final_formatted}");
                }
            }
            else
            {
                Console.WriteLine("Нет доступных данных о игре.");
            }
        }
    }
}
