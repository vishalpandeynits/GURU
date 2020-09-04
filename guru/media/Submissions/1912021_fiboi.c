#include <stdio.h>
#include <string.h>
// This program can calculate fibonaci numbers upto 2000
int main()
{
    //creating a 2d array  for storing all the fibbo no that will be pre-calculated
    char fibo[2100][500];

    // At first the code will automatically calculate fibbo no's upto 2000 terms
    fibo[0][0] = '0';
    fibo[1][0] = '1';

    int n1, n2,i,j; //for calculating the length of the array of stored fibbo nos
    
    //This loop will calculate the fibo nos and store it in an array
    for (i = 0; i <= 2000; i++)
    {

        n1 = strlen(fibo[i]);
        n2 = strlen(fibo[i + 1]);

        int carry = 0;
        for (j = 0; j < n1; j++)
        {
            int sum = ((fibo[i][j] - '0') + (fibo[i + 1][j] - '0') + carry);
            fibo[i + 2][j] = sum % 10 + '0';

            carry = sum / 10;
        }
        // and for adding the remaining digits in n2,string1
        for (j = n1; j < n2; j++)
        {
            int sum = ((fibo[i + 1][j] - '0') + carry);
            fibo[i + 2][j] = sum % 10 + '0';
            carry = sum / 10;
        }
        //adding remaining carry
        if (carry)
            fibo[i + 2][n2] = carry + '0';
    }

    //after compilation  of 1000Th fiboo series it will ask for your desired fibbo no term
    int n;
    printf("Array indexing starts from 0.\n");
    printf("Which term of the fibonacci series do you want\n ");
    
    while(1){
    	scanf("%d", &n);
    	if (n<2000 && n>0) break;
    	else printf("Please enter a number between 1 and 2000.\n");
    	
	}
    
    
    int n3 = strlen(fibo[n]);

    printf("The required term is \n");

    for (i = n3 - 1; i >= 0; i--)
        printf("%d", fibo[n][i] - 48);
        
    return 0;
}
