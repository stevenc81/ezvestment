
Value Proposition
=
Let's not repeat what we knew already. Wrap up in one sentence and it would be: 

>A super simple and cheap investment tool that helps you to make tailored investment choices w/o having to listen to lame advisors. 

Okay this sentence is a bit long but you get it. I do think this service highly demanded in everywhere. In Taiwan almost everyone is hardwired to buy an insurance policy when they get their first job. It's perplexing to me but it's true. Oh, they usually get the hybrid (health + investment) insurance policy so that affirms the demand is strong.

How it's Done
=
As I waded through more info about WF and BM I grew confidence that this is not as hard as I originally anticipated. Not I'm saying it's much easier now but I've overestimated some difficult steps. Here is why

Inventory
-
WF almost exclusively uses the ETFs from [Vanguard](https://personal.vanguard.com/us/funds/etf) whilst they claimed they receive no compensation whatsoever and Vanguard simply comes out of the top when they try to get the best mix. As I dug deeper I notice Vanguard only has 50 ETFs spanning low to high risk level. Those ETFs can potentially be US Stocks, Foreign Stocks, Emerging Markets, Real Estate, Natural Resources and Bonds. Now that will save us shit loads of time since we only need to deal one ETF provider and so far the users are happy with this inventory. This tells us the users don't want to have too many choices anyway. The whole point is to be simple and effective so we should spare them from the details.

Combination/Mix
-
Here is where the magic comes it. Our partner in PWM has to set up different investment mixes to 10 risk levels. Of course from our inventory. I don't see any immediate needs to make it more granular. I don't know how these hotshots PWMs do their magic but it will be hardcoded in the product and shall be updated at least in weekly basis. These mixes are subject to market changes so the freshness is probably **THE MOST IMPORTANT** thing in our business. 

MPT
-
[MPT in Java](http://ojalgo.org/modern_portfolio_theory.html), [MPT in Python](http://travisvaught.blogspot.tw/2011/09/modern-portfolio-theory-python.html), taa-da we are done. The only part remains to be done is how to assess user's risk tolerance.

Assessing Users
-
I haven't found any good ways to do this yet. But I have tried WF today they asked 10 simple questions like how much I make a year, how much I have in saving (these predicts if I will commit a suicide if bear bites hard) and if I would invest more when the market is low and I lose 10% principle (gauge my aggressiveness). I ended up with 8/10.

Portfolio Management
-
It's transparent to users as if they are managing the funds themselves. Of course that's the right way to do. WF uses [Apex](https://online.apexclearing.com). I can't imagine that being to hard to integrate to, yet.

Quote from [Investor Junkies](http://investorjunkie.com/)
>The actual portfolio is held with Apex Clearing Corporation. This is no different than having your account with a discount broker like TradeKing, who also uses Apex.

Pricing Plans
-
- For WF, you need 5k to play the game and 100k for tax-loss harvesting
- For BM, you need to deposit $100 monthly to play the game
  - 10k for .25% fee, or 
  - 100k for .15% fee

Strategic Partnership
=
We need

1. A world class, legendary, ass kicking PWM
2. Vanguard
3. Apex

MVP
=
This is where everything starts. Like I said earlier I started to think this might not be difficult to do after all. All we need are

1. Few questions to access users
2. Signup process
3. Predefined mix for the user
4. Fancy sleek looking UI for users to set their investment goals and ways to get there by adjusting the mix
5. Automated reporting on the yields
6. Security, security and security
6. I'm sure I missed a whole lot here, get back to you tomorrow.

Key Features
-
I've identified the key thing in the product is…**FANCY UI**. I'm sure pricing, and ass kicking PWM are all other important factors but that can come later after MVP, also the security.

Team
-
- 1 front-end dev
- 1 external service dev
- 1 rockstar back-end dev who has knowledge of security. When I say rockstar I mean it.
- 1 PWM
- 1 PM to figure out the pricing table, features, design and work with the team.

Timeline
-
First of all I want to be clear, w/o knowing the actual scope it's hard for me to make an accurate estimate. So don't fire me if the estimate is off because i'm pretty sure it will be. I'm mere offering my gut feeling at this moment.

I'd say *3 months* for now. With a high chance of delay or having to expand the team. We will probably need 2 front-end devs.

References
=

http://investorjunkie.com/16817/wealthfront-review/
http://investorjunkie.com/8745/betterment-review/
http://investorjunkie.com/13093/personal-capital-review/
https://personal.vanguard.com/us/funds/etf
https://www.wealthfront.com/jobs
http://www.youtube.com/watch?feature=player_embedded&v=2qOYDpF24cs#!
https://wwws.betterment.com/app/#summary