c: public(uint256)

@public
@constant
def get() -> uint256:
    return self.c

@public
def up():
    self.c += 1
