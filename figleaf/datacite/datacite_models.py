# generated by datamodel-codegen:
#   filename:  https://raw.githubusercontent.com/datacite/schema/732cc7ef29f4cad4d6adfac83544133cd57a2e5e/source/json/kernel-4.3/datacite_4.3_schema.json
#   timestamp: 2023-04-06T11:50:47+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import AnyUrl, BaseModel, Field, confloat


class Identifier(BaseModel):
    identifier: str
    identifierType: str


class Subject(BaseModel):
    subject: str
    subjectScheme: Optional[str] = None
    schemeURI: Optional[AnyUrl] = None
    valueURI: Optional[AnyUrl] = None
    lang: Optional[str] = None


class AlternateIdentifier(BaseModel):
    alternateIdentifier: str
    alternateIdentifierType: str


class RightsListItem(BaseModel):
    rights: Optional[str] = None
    rightsURI: Optional[AnyUrl] = None
    rightsIdentifier: Optional[str] = None
    rightsIdentifierScheme: Optional[str] = None
    schemeURI: Optional[AnyUrl] = None
    lang: Optional[str] = None


class NameType(Enum):
    Organizational = 'Organizational'
    Personal = 'Personal'


class NameIdentifier(BaseModel):
    nameIdentifier: str
    nameIdentifierScheme: str
    schemeURI: Optional[AnyUrl] = None


class NameIdentifiers(BaseModel):
    __root__: List[NameIdentifier] = Field(..., unique_items=True)


class Affiliation(BaseModel):
    affiliation: str


class Affiliations(BaseModel):
    __root__: List[Affiliation] = Field(..., unique_items=True)


class TitleType(Enum):
    AlternativeTitle = 'AlternativeTitle'
    Subtitle = 'Subtitle'
    TranslatedTitle = 'TranslatedTitle'
    Other = 'Other'


class ContributorType(Enum):
    ContactPerson = 'ContactPerson'
    DataCollector = 'DataCollector'
    DataCurator = 'DataCurator'
    DataManager = 'DataManager'
    Distributor = 'Distributor'
    Editor = 'Editor'
    HostingInstitution = 'HostingInstitution'
    Producer = 'Producer'
    ProjectLeader = 'ProjectLeader'
    ProjectManager = 'ProjectManager'
    ProjectMember = 'ProjectMember'
    RegistrationAgency = 'RegistrationAgency'
    RegistrationAuthority = 'RegistrationAuthority'
    RelatedPerson = 'RelatedPerson'
    Researcher = 'Researcher'
    ResearchGroup = 'ResearchGroup'
    RightsHolder = 'RightsHolder'
    Sponsor = 'Sponsor'
    Supervisor = 'Supervisor'
    WorkPackageLeader = 'WorkPackageLeader'
    Other = 'Other'


class Date(BaseModel):
    __root__: Union[Any, Any, Any, Any, Any, Any, Any, Any]


class DateType(Enum):
    Accepted = 'Accepted'
    Available = 'Available'
    Copyrighted = 'Copyrighted'
    Collected = 'Collected'
    Created = 'Created'
    Issued = 'Issued'
    Submitted = 'Submitted'
    Updated = 'Updated'
    Valid = 'Valid'
    Withdrawn = 'Withdrawn'
    Other = 'Other'


class ResourceTypeGeneral(Enum):
    Audiovisual = 'Audiovisual'
    Collection = 'Collection'
    DataPaper = 'DataPaper'
    Dataset = 'Dataset'
    Event = 'Event'
    Image = 'Image'
    InteractiveResource = 'InteractiveResource'
    Model = 'Model'
    PhysicalObject = 'PhysicalObject'
    Service = 'Service'
    Software = 'Software'
    Sound = 'Sound'
    Text = 'Text'
    Workflow = 'Workflow'
    Other = 'Other'


class RelatedIdentifierType(Enum):
    ARK = 'ARK'
    arXiv = 'arXiv'
    bibcode = 'bibcode'
    DOI = 'DOI'
    EAN13 = 'EAN13'
    EISSN = 'EISSN'
    Handle = 'Handle'
    IGSN = 'IGSN'
    ISBN = 'ISBN'
    ISSN = 'ISSN'
    ISTC = 'ISTC'
    LISSN = 'LISSN'
    LSID = 'LSID'
    PMID = 'PMID'
    PURL = 'PURL'
    UPC = 'UPC'
    URL = 'URL'
    URN = 'URN'
    w3id = 'w3id'


class RelationType(Enum):
    IsCitedBy = 'IsCitedBy'
    Cites = 'Cites'
    IsSupplementTo = 'IsSupplementTo'
    IsSupplementedBy = 'IsSupplementedBy'
    IsContinuedBy = 'IsContinuedBy'
    Continues = 'Continues'
    IsDescribedBy = 'IsDescribedBy'
    Describes = 'Describes'
    HasMetadata = 'HasMetadata'
    IsMetadataFor = 'IsMetadataFor'
    HasVersion = 'HasVersion'
    IsVersionOf = 'IsVersionOf'
    IsNewVersionOf = 'IsNewVersionOf'
    IsPreviousVersionOf = 'IsPreviousVersionOf'
    IsPartOf = 'IsPartOf'
    HasPart = 'HasPart'
    IsReferencedBy = 'IsReferencedBy'
    References = 'References'
    IsDocumentedBy = 'IsDocumentedBy'
    Documents = 'Documents'
    IsCompiledBy = 'IsCompiledBy'
    Compiles = 'Compiles'
    IsVariantFormOf = 'IsVariantFormOf'
    IsOriginalFormOf = 'IsOriginalFormOf'
    IsIdenticalTo = 'IsIdenticalTo'
    IsReviewedBy = 'IsReviewedBy'
    Reviews = 'Reviews'
    IsDerivedFrom = 'IsDerivedFrom'
    IsSourceOf = 'IsSourceOf'
    IsRequiredBy = 'IsRequiredBy'
    Requires = 'Requires'
    IsObsoletedBy = 'IsObsoletedBy'
    Obsoletes = 'Obsoletes'


class DescriptionType(Enum):
    Abstract = 'Abstract'
    Methods = 'Methods'
    SeriesInformation = 'SeriesInformation'
    TableOfContents = 'TableOfContents'
    TechnicalInfo = 'TechnicalInfo'
    Other = 'Other'


class Longitude(BaseModel):
    __root__: confloat(ge=-180.0, le=180.0)


class Latitude(BaseModel):
    __root__: confloat(ge=-90.0, le=90.0)


class FunderIdentifierType(Enum):
    ISNI = 'ISNI'
    GRID = 'GRID'
    Crossref_Funder_ID = 'Crossref Funder ID'
    Other = 'Other'


class Types(BaseModel):
    resourceType: str
    resourceTypeGeneral: ResourceTypeGeneral


class Creator(BaseModel):
    name: str
    nameType: Optional[NameType] = None
    givenName: Optional[str] = None
    familyName: Optional[str] = None
    nameIdentifiers: Optional[NameIdentifiers] = None
    affiliations: Optional[Affiliations] = None
    lang: Optional[str] = None


class Title(BaseModel):
    title: str
    titleType: Optional[TitleType] = None
    lang: Optional[str] = None


class Contributor(BaseModel):
    contributorType: ContributorType
    name: str
    nameType: Optional[NameType] = None
    givenName: Optional[str] = None
    familyName: Optional[str] = None
    nameIdentifiers: Optional[NameIdentifiers] = None
    affiliations: Optional[Affiliations] = None
    lang: Optional[str] = None


class DateModel(BaseModel):
    date: Date
    dateType: DateType
    dateInformation: Optional[str] = None


class RelatedIdentifier(BaseModel):
    relatedIdentifier: str
    relatedIdentifierType: RelatedIdentifierType
    relationType: RelationType
    relatedMetadataScheme: Optional[str] = None
    schemeURI: Optional[AnyUrl] = None
    schemeType: Optional[str] = None
    resourceTypeGeneral: Optional[ResourceTypeGeneral] = None


class Description(BaseModel):
    description: str
    descriptionType: DescriptionType
    lang: Optional[str] = None


class GeoLocationBox(BaseModel):
    westBoundLongitude: Longitude
    eastBoundLongitude: Longitude
    southBoundLatitude: Latitude
    northBoundLatitude: Latitude


class FundingReference(BaseModel):
    funderName: str
    funderIdentifier: Optional[str] = None
    funderIdentifierType: Optional[FunderIdentifierType] = None
    awardNumber: Optional[str] = None
    awardURI: Optional[AnyUrl] = None
    awardTitle: Optional[str] = None


class GeoLocationPoint(BaseModel):
    pointLongitude: Longitude
    pointLatitude: Latitude


class GeoLocationPolygon(BaseModel):
    polygonPoints: List[GeoLocationPoint] = Field(..., min_items=4)
    inPolygonPoint: Optional[GeoLocationPoint] = None


class GeoLocation(BaseModel):
    geoLocationPlace: Optional[str] = None
    geoLocationPoint: Optional[GeoLocationPoint] = None
    geoLocationBox: Optional[GeoLocationBox] = None
    geoLocationPolygons: Optional[List[GeoLocationPolygon]] = Field(
        None, unique_items=True
    )


class Model(BaseModel):
    types: Types
    identifiers: List[Identifier] = Field(..., min_items=1, unique_items=True)
    creators: List[Creator] = Field(..., min_items=1, unique_items=True)
    titles: List[Title] = Field(..., min_items=1, unique_items=True)
    publisher: str
    publicationYear: str
    subjects: Optional[List[Subject]] = Field(None, unique_items=True)
    contributors: Optional[List[Contributor]] = Field(None, unique_items=True)
    dates: Optional[List[DateModel]] = Field(None, unique_items=True)
    language: Optional[str] = None
    alternateIdentifiers: Optional[List[AlternateIdentifier]] = Field(
        None, unique_items=True
    )
    relatedIdentifiers: Optional[List[RelatedIdentifier]] = Field(
        None, unique_items=True
    )
    sizes: Optional[List[str]] = Field(None, unique_items=True)
    formats: Optional[List[str]] = Field(None, unique_items=True)
    version: Optional[str] = None
    rightsList: Optional[List[RightsListItem]] = Field(None, unique_items=True)
    descriptions: Optional[List[Description]] = Field(None, unique_items=True)
    geoLocations: Optional[List[GeoLocation]] = Field(None, unique_items=True)
    fundingReferences: Optional[List[FundingReference]] = Field(None, unique_items=True)
    schemaVersion: str = Field('http://datacite.org/schema/kernel-4', const=True)