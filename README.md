# fixer

This is an utility built with spare time. It is supposed to be used to quickly know the foreign exchange rate for common currencies, and it can also calculate the amount for you.

Usage:

"How much is 100 BRL in USD?"

    λ fixer brl usd 100

Should give you something like:

     - - - - - - - - - - - - - - - - - - - -
    BRL 100.0 is worth approximately USD 30.362000000000002
     - - - - - - - - - - - - - - - - - - - -

You can also query for all available currencies in fixer.io giving a base currency:

    λ fixer usd
     - - - - - - - - - - - - - - - - - - - -
    AUD: 1.3149
    BGN: 1.7138
    BRL: 3.2936
    CAD: 1.2974
    CHF: 0.96241
    CNY: 6.799
    CZK: 22.852
    DKK: 6.5169
    GBP: 0.77539
    HKD: 7.8111
    HRK: 6.4978
    HUF: 270.22
    IDR: 13408.0
    ILS: 3.529
    INR: 64.578
    JPY: 113.74
    KRW: 1155.0
    MXN: 18.182
    MYR: 4.2985
    NOK: 8.3783
    NZD: 1.373
    PHP: 50.636
    PLN: 3.7086
    RON: 4.0188
    RUB: 60.392
    SEK: 8.4258
    SGD: 1.3811
    THB: 34.08
    TRY: 3.6335
    ZAR: 13.376
    EUR: 0.87627
     - - - - - - - - - - - - - - - - - - - -

And query the simple conversion, of course:

    λ fixer usd brl
     - - - - - - - - - - - - - - - - - - - -
    USD is worth approximately BRL 3.2936
     - - - - - - - - - - - - - - - - - - - -

Visit the website that hosts this wonderful API: http://fixer.io/

---

# License

The MIT License (MIT)

Copyright (c) 2017 Renato Oliveira

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.