# Plan

## DB Structure
* User
  * Email
  * Username
  * Password
  * Cash
  * Assets
    * Should original purchase price of assets be included here
      * Percent increase? (probably should be calculated)
* Trades
  * User
  * Pair
    * USD/EUR, USD/MSFT, etc.
  * Price
  * Amount received
  * Amount paid
* Prices
  * Pair
  * Price
    * Most recent fetched price
  * Time when price was fetched - "fetchtime"
    * If a user requests the price of an asset and that price was updated within the last minute, don't call the api
  * Maybe there should be a counter to see how often the price is fetched?

## Key ideas
* Value of user portfolio is calculated by multiplying asset quantity by the price in the database
  * If price in database is outdated, ask the api to refresh it
* Executing an order creates a new trade item and adds(or removes) the assets from the user's assets list
* Probably need a limit on API requests to prevent people from taking advantage of my API
  * Should the api be able to get the price of the stock?
    * Probably, limit to once per minute?
    * Could just ask the user to get price data from other APIs if they are doing algorithmic trading
    * Could try giving free data api but stop if it becomes impossible to manage
* Later, the user should be able to have multiple portfolios in case they bankrupt themselves or just want to try something else

## TODO
* Create the api first, then create a frontend
