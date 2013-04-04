using System;

public class Program
{
    public static void Main(string[] args)
    {
        Console.Write("parametros: ");
        foreach (string s in args) {
            Console.Write(s + " ");
        }
        Console.WriteLine();
    }
} 
