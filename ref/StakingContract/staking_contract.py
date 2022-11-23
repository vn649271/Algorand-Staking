#!/usr/bin/env python3

from pyteal import *

def approval_program():
    creator_key = Bytes("creator")
    is_creator = Txn.sender() == App.globalGet(creator_key)

    @Subroutine(TealType.none)
    def unstake(client: Expr, unstakeAmount: Expr) -> Expr:
        return Seq(
            Assert(unstakeAmount < TxnField.amount - Global.min_txn_fee()),
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.Payment,
                    TxnField.amount: unstakeAmount - Global.min_txn_fee(),
                    TxnField.receiver: client,
                }
            ),
            InnerTxnBuilder.Submit(),
        )
    
    handle_creation = Seq([
        App.globalPut(creator_key, Txn.sender()),
        App.globalPut(Bytes("Sum"), Int(0)),
        Return(Int(1))
    ])

    handle_optin = Return(Int(0))

    handle_closeout = Return(Int(0))

    handle_updateapp = Return(Int(0))

    handle_deleteapp = Return(Int(0))

    scratchSum = ScratchVar(TealType.uint64)
    scratchStake = ScratchVar(TealType.uint64)
    
    on_stake = Seq([
        Assert(Txn.application_args.length() == Int(2)),
        Assert(Txn.type_enum() == TxnType.Payment),
        scratchStake.store(Txn.amount()),
        scratchSum.store(App.globalGet(Bytes("Sum"))),
        App.globalPut(Bytes("Sum"), scratchSum.load() + scratchStake.load()),
        App.globalPut(Txn.sender(), scratchStake.load()),
        Return(Int(1))
    ])

    handle_noop = Cond(
        [

            And(
                Global.group_size() == Int(1),
	            Txn.application_args[0] == Bytes("stake")
            ),
    	    on_stake
    	],
    )


    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )
    # Mode.Application specifies that this is a smart contract
    return compileTeal(program, Mode.Application, version=4)


def clear_state_program():
    program = Return(Int(1))
    # Mode.Application specifies that this is a smart contract
    return compileTeal(program, Mode.Application, version=4)

# print out the results
print(approval_program())
print(clear_state_program())
