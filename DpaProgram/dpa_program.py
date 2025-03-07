from pydantic import BaseModel, Field
from typing import List, Optional

class FirstTimeHomeBuyerRequirement(BaseModel):
    requirement: str = Field(default="No")
    description: Optional[str] = Field(default="") 

class DpaDownPaymentBorrowerContribution(BaseModel):
    description: Optional[str] = Field(default=None) 
    isContributionRequired: bool = Field(default=False)

class FirstMortgageProduct(BaseModel):
    firstMortgageProductName: str = Field(default="") 
    customType: List[str] = Field(defaul=[]) 

class HouseholdOccupantLimits(BaseModel):
    limitType: str = Field(default=None)
    limitLowerBound: int = Field(default=None)
    limitUpperBound: int = Field(default=None)

class Location(BaseModel):
    listLocationBy: str = Field(default="counties")
    listIndividually: bool = Field(default=True)
    localDetails: List[str] = Field(default=[])

class ProgramDetails(BaseModel):
    maximumLienPosition: int = Field(default=2)

class ProgramFunds(BaseModel):
    fundingIsUnlimited: bool = Field(default=True)

class MaximumSalesPrice(BaseModel):
    cities: List[str] = Field(default=[])
    counties: List[str] = Field(default=[])
    area: str = Field(default="")
    maxPurchasePrice: str = Field(default="")
    products: str = Field(default="")
    types: str = Field(default="")
    propertyType: List[str] = Field(default=[])
    targeted: bool = Field(default=False)
    description: str = Field(default="")

class Occupants(BaseModel):
    limitType: str = Field(default="")
    limitLowerBound: str = Field(default="")
    limitUpperBound: str = Field(default="")

class OccupantLimit(BaseModel):
    occupants: Occupants = Field(default=[])
    limit: str = Field(default="")

class HouseholdIncomeLimits(BaseModel):
    cities: List[str] = Field(default=[])
    counties: List[str] = Field(default=[])
    occupantLimits: List[OccupantLimit] = Field(default=[])
    products: str = Field(default="")
    types: str = Field(default="")
    targeted: bool = Field(default=False)
    description: str = Field(default="")
    area: str = Field(default="")


class CreditScoreRestriction(BaseModel):
    counties: List[str] = Field(default=[])
    cities: List[str] = Field(default=[])
    score: str = Field(default="")
    propertyType: List[str] = Field(default=[])
    products: str = Field(default="")
    types: str = Field(default="")
    ltv: str = Field(default="")
    tltv: str = Field(default="")
    dti: str = Field(default="")
    underwriting: List[str] = Field(default=[])


class LenderInfo(BaseModel):
    lenderNames: List[str] = Field(default=[])


class DpaProgramDocument(BaseModel):
    documentDetails: List[str] = Field(default=[])

class DpaLoanForgivenessCondition(BaseModel):
    applicable: bool = Field(default=False)
    description: str = Field(default="")


class DpaProgram(BaseModel):
    description: str = Field(default="")
    programName: str = Field(default="")
    firstTimeHomeBuyerRequirement: FirstTimeHomeBuyerRequirement = Field(default={})
    dpaDownPaymentBorrowerContribution: DpaDownPaymentBorrowerContribution = Field(default={})
    firstMortgageProduct: List[FirstMortgageProduct] = Field(default=[])
    householdOccupantLimits: List[HouseholdOccupantLimits] = Field(default=[])
    isTargetedIncomeLimit: bool = Field(default=False)
    isTargetedPurchasePriceLimit: bool = Field(default=False)
    location: Location = Field(default={})
    isSeperateTable: bool = Field(default=True)
    programType: str = Field(default="loan")
    details: ProgramDetails = Field(default={})
    programFunds: ProgramFunds = Field(default={})
    loanType: dict = Field(default={})
    allowedLoanPurposes: List[str] = Field(default=[])
    programServicingEntities: List[str] = Field(default=[])
    firstMortgageRequirements: List[str] = Field(default=[])
    approvedHomeBuyerEducationProvider: List[str] = Field(default=[])
    hasDeedOrResaleRestriction: bool = Field(default=False)
    ownerOccupancyRequirement: bool = Field(default=False)
    balloonPayment: bool = Field(default=False)
    heloc: bool = Field(default=False)
    negativeAmortization: bool = Field(default=False)
    dpaLoanForgivenessCondition: DpaLoanForgivenessCondition = Field(default={})
    maximumSalesPrice: List[MaximumSalesPrice] = Field(default=[])
    householdIncomeLimits: List[HouseholdIncomeLimits] = Field(default=[])
    creditScoreRestrictions: List[CreditScoreRestriction] = Field(default=[])
    lenderInfo: LenderInfo = Field(default={})
    dpaProgramDocuments: List[DpaProgramDocument] = Field(default=[])
