ABI = [
    # Constructor
    {
        "inputs": [
            {"internalType": "address", "name": "_cakeTokenAddress", "type": "address"},
            {"internalType": "bool", "name": "_OnoutFeeEnabled", "type": "bool"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },

    # Event: Token recovery by admin
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "address", "name": "token", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "AdminTokenRecovery",
        "type": "event"
    },

    # Event: Lottery closed
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "lotteryId", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "firstTicketIdNextLottery", "type": "uint256"}
        ],
        "name": "LotteryClose",
        "type": "event"
    },

    # Event: Funds injected into a lottery
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "lotteryId", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "injectedAmount", "type": "uint256"}
        ],
        "name": "LotteryInjection",
        "type": "event"
    },

    # Event: Winning lottery numbers drawn
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "lotteryId", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "finalNumber", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "countWinningTickets", "type": "uint256"}
        ],
        "name": "LotteryNumberDrawn",
        "type": "event"
    },

    # Event: Lottery opened
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "lotteryId", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "startTime", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "endTime", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "priceTicketInCake", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "firstTicketId", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "injectedAmount", "type": "uint256"}
        ],
        "name": "LotteryOpen",
        "type": "event"
    },

    # Event: Operator, treasury, and injector addresses updated
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "address", "name": "operator", "type": "address"},
            {"indexed": False, "internalType": "address", "name": "treasury", "type": "address"},
            {"indexed": False, "internalType": "address", "name": "injector", "type": "address"}
        ],
        "name": "NewOperatorAndTreasuryAndInjectorAddresses",
        "type": "event"
    },

    # Event: Ownership transferred
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },

    # Event: Tickets claimed
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "claimer", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
            {"indexed": True, "internalType": "uint256", "name": "lotteryId", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "numberTickets", "type": "uint256"}
        ],
        "name": "TicketsClaim",
        "type": "event"
    },

    # Event: Tickets purchased
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "buyer", "type": "address"},
            {"indexed": True, "internalType": "uint256", "name": "lotteryId", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "numberTickets", "type": "uint256"}
        ],
        "name": "TicketsPurchase",
        "type": "event"
    },

    # Function: MAX_LENGTH_LOTTERY
    {
        "inputs": [],
        "name": "MAX_LENGTH_LOTTERY",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: MAX_TREASURY_FEE
    {
        "inputs": [],
        "name": "MAX_TREASURY_FEE",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: MIN_DISCOUNT_DIVISOR
    {
        "inputs": [],
        "name": "MIN_DISCOUNT_DIVISOR",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: MIN_LENGTH_LOTTERY
    {
        "inputs": [],
        "name": "MIN_LENGTH_LOTTERY",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: OnoutAddress
    {
        "inputs": [],
        "name": "OnoutAddress",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: OnoutFeeEnabled
    {
        "inputs": [],
        "name": "OnoutFeeEnabled",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Buy tickets
    {
        "inputs": [
            {"internalType": "uint256", "name": "_lotteryId", "type": "uint256"},
            {"internalType": "uint32[]", "name": "_ticketNumbers", "type": "uint32[]"}
        ],
        "name": "buyTickets",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Get the cakeToken contract address
    {
        "inputs": [],
        "name": "cakeToken",
        "outputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Calculate total price for bulk tickets
    {
        "inputs": [
            {"internalType": "uint256", "name": "_discountDivisor", "type": "uint256"},
            {"internalType": "uint256", "name": "_priceTicket", "type": "uint256"},
            {"internalType": "uint256", "name": "_numberTickets", "type": "uint256"}
        ],
        "name": "calculateTotalPriceForBulkTickets",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "pure",
        "type": "function"
    },

    # Function: Claim tickets
    {
        "inputs": [
            {"internalType": "uint256", "name": "_lotteryId", "type": "uint256"},
            {"internalType": "uint256[]", "name": "_ticketIds", "type": "uint256[]"},
            {"internalType": "uint32[]", "name": "_brackets", "type": "uint32[]"}
        ],
        "name": "claimTickets",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Close a lottery
    {
        "inputs": [{"internalType": "uint256", "name": "_lotteryId", "type": "uint256"}],
        "name": "closeLottery",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Get current lottery ID
    {
        "inputs": [],
        "name": "currentLotteryId",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Get current ticket ID
    {
        "inputs": [],
        "name": "currentTicketId",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Draw final number and make lottery claimable
    {
        "inputs": [
            {"internalType": "uint256", "name": "_lotteryId", "type": "uint256"},
            {"internalType": "bytes32", "name": "_seed", "type": "bytes32"},
            {"internalType": "bool", "name": "_autoInjection", "type": "bool"}
        ],
        "name": "drawFinalNumberAndMakeLotteryClaimable",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Inject funds into a lottery
    {
        "inputs": [
            {"internalType": "uint256", "name": "_lotteryId", "type": "uint256"},
            {"internalType": "uint256", "name": "_amount", "type": "uint256"}
        ],
        "name": "injectFunds",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Get the injector address
    {
        "inputs": [],
        "name": "injectorAddress",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Get the maximum number of tickets that can be bought or claimed
    {
        "inputs": [],
        "name": "maxNumberTicketsPerBuyOrClaim",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Get the maximum price per ticket in cake
    {
        "inputs": [],
        "name": "maxPriceTicketInCake",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Get the minimum price per ticket in cake
    {
        "inputs": [],
        "name": "minPriceTicketInCake",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Get the numbers count
    {
        "inputs": [],
        "name": "numbersCount",
        "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Get the operator address
    {
        "inputs": [],
        "name": "operatorAddress",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Get the pending injection for the next lottery
    {
        "inputs": [],
        "name": "pendingInjectionNextLottery",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Recover wrongly sent tokens
    {
        "inputs": [
            {"internalType": "address", "name": "_tokenAddress", "type": "address"},
            {"internalType": "uint256", "name": "_tokenAmount", "type": "uint256"}
        ],
        "name": "recoverWrongTokens",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Renounce ownership
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Set the maximum number of tickets that can be bought or claimed
    {
        "inputs": [
            {"internalType": "uint256", "name": "_maxNumberTicketsPerBuy", "type": "uint256"}
        ],
        "name": "setMaxNumberTicketsPerBuy",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Set the minimum and maximum ticket price in cake
    {
        "inputs": [
            {"internalType": "uint256", "name": "_minPriceTicketInCake", "type": "uint256"},
            {"internalType": "uint256", "name": "_maxPriceTicketInCake", "type": "uint256"}
        ],
        "name": "setMinAndMaxTicketPriceInCake",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Set the numbers count
    {
        "inputs": [
            {"internalType": "uint32", "name": "_numbersCount", "type": "uint32"}
        ],
        "name": "setNumbersCount",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Set the Onout fee address
    {
        "inputs": [
            {"internalType": "address", "name": "_newFeeAddress", "type": "address"}
        ],
        "name": "setOnoutAddress",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Set whether Onout fee is enabled
    {
        "inputs": [
            {"internalType": "bool", "name": "_value", "type": "bool"}
        ],
        "name": "setOnoutFeeEnabled",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Set operator addresses
    {
        "inputs": [
            {"internalType": "address", "name": "_operatorAddress", "type": "address"}
        ],
        "name": "setOperatorAddresses",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Set operator, treasury, and injector addresses
    {
        "inputs": [
            {"internalType": "address", "name": "_operatorAddress", "type": "address"},
            {"internalType": "address", "name": "_treasuryAddress", "type": "address"},
            {"internalType": "address", "name": "_injectorAddress", "type": "address"}
        ],
        "name": "setOperatorAndTreasuryAndInjectorAddresses",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Start a new lottery
    {
        "inputs": [
            {"internalType": "uint256", "name": "_endTime", "type": "uint256"},
            {"internalType": "uint256", "name": "_priceTicketInCake", "type": "uint256"},
            {"internalType": "uint256", "name": "_discountDivisor", "type": "uint256"},
            {"internalType": "uint256[6]", "name": "_rewardsBreakdown", "type": "uint256[6]"},
            {"internalType": "uint256", "name": "_treasuryFee", "type": "uint256"}
        ],
        "name": "startLottery",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Get the owner address
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Transfer ownership
    {
        "inputs": [
            {"internalType": "address", "name": "newOwner", "type": "address"}
        ],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },

    # Function: Get the treasury address
    {
        "inputs": [],
        "name": "treasuryAddress",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Get the current lottery ID (view-only)
    {
        "inputs": [],
        "name": "viewCurrentLotteryId",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Get lottery details for a specific lottery ID (view-only)
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_lotteryId",
                "type": "uint256"
            }
        ],
        "name": "viewLottery",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "enum PancakeSwapLottery.Status",
                        "name": "status",
                        "type": "uint8"
                    },
                    {
                        "internalType": "uint256",
                        "name": "startTime",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "endTime",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "priceTicketInCake",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "discountDivisor",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256[6]",
                        "name": "rewardsBreakdown",
                        "type": "uint256[6]"
                    },
                    {
                        "internalType": "uint256",
                        "name": "treasuryFee",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256[6]",
                        "name": "cakePerBracket",
                        "type": "uint256[6]"
                    },
                    {
                        "internalType": "uint256[6]",
                        "name": "countWinnersPerBracket",
                        "type": "uint256[6]"
                    },
                    {
                        "internalType": "uint256",
                        "name": "firstTicketId",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "firstTicketIdNextLottery",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "amountCollectedInCake",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint32",
                        "name": "finalNumber",
                        "type": "uint32"
                    }
                ],
                "internalType": "struct PancakeSwapLottery.Lottery",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Get numbers and statuses for a list of ticket IDs (view-only)
    {
        "inputs": [
            {"internalType": "uint256[]", "name": "_ticketIds", "type": "uint256[]"}
        ],
        "name": "viewNumbersAndStatusesForTicketIds",
        "outputs": [
            {"internalType": "uint32[]", "name": "", "type": "uint32[]"},
            {"internalType": "bool[]", "name": "", "type": "bool[]"}
        ],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Get rewards for a specific ticket ID (view-only)
    {
        "inputs": [
            {"internalType": "uint256", "name": "_lotteryId", "type": "uint256"},
            {"internalType": "uint256", "name": "_ticketId", "type": "uint256"},
            {"internalType": "uint32", "name": "_bracket", "type": "uint32"}
        ],
        "name": "viewRewardsForTicketId",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: View user info for a specific lottery ID (view-only)
    {
        "inputs": [
            {"internalType": "address", "name": "_user", "type": "address"},
            {"internalType": "uint256", "name": "_lotteryId", "type": "uint256"},
            {"internalType": "uint256", "name": "_cursor", "type": "uint256"},
            {"internalType": "uint256", "name": "_size", "type": "uint256"}
        ],
        "name": "viewUserInfoForLotteryId",
        "outputs": [
            {"internalType": "uint256[]", "name": "", "type": "uint256[]"},
            {"internalType": "uint32[]", "name": "", "type": "uint32[]"},
            {"internalType": "bool[]", "name": "", "type": "bool[]"},
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },

    # Function: Withdraw funds from the bank
    {
        "inputs": [
            {"internalType": "uint256", "name": "_tokenAmount", "type": "uint256"}
        ],
        "name": "withdrawBank",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

WETH_ABI = [
    # name Function
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    # approve Function
    {
        "constant": False,
        "inputs": [{"name": "guy", "type": "address"}, {"name": "wad", "type": "uint256"}],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    # totalSupply Function
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    # transferFrom Function
    {
        "constant": False,
        "inputs": [{"name": "src", "type": "address"}, {"name": "dst", "type": "address"}, {"name": "wad", "type": "uint256"}],
        "name": "transferFrom",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    # withdraw Function
    {
        "constant": False,
        "inputs": [{"name": "wad", "type": "uint256"}],
        "name": "withdraw",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    # decimals Function
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    # balanceOf Function
    {
        "constant": True,
        "inputs": [{"name": "", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    # symbol Function
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    # transfer Function
    {
        "constant": False,
        "inputs": [{"name": "dst", "type": "address"}, {"name": "wad", "type": "uint256"}],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    # deposit Function
    {
        "constant": False,
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "payable": True,
        "stateMutability": "payable",
        "type": "function",
    },
    # allowance Function
    {
        "constant": True,
        "inputs": [{"name": "", "type": "address"}, {"name": "", "type": "address"}],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    # Fallback Function
    {
        "payable": True,
        "stateMutability": "payable",
        "type": "fallback",
    },
    # Approval Event
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "src", "type": "address"},
            {"indexed": True, "name": "guy", "type": "address"},
            {"indexed": False, "name": "wad", "type": "uint256"},
        ],
        "name": "Approval",
        "type": "event",
    },
    # Transfer Event
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "src", "type": "address"},
            {"indexed": True, "name": "dst", "type": "address"},
            {"indexed": False, "name": "wad", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    },
    # Deposit Event
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "dst", "type": "address"},
            {"indexed": False, "name": "wad", "type": "uint256"},
        ],
        "name": "Deposit",
        "type": "event",
    },
    # Withdrawal Event
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "src", "type": "address"},
            {"indexed": False, "name": "wad", "type": "uint256"},
        ],
        "name": "Withdrawal",
        "type": "event",
    },
]










