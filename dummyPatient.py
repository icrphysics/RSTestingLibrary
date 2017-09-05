"""
Reconstruct a dummy patient for testing purposes.

To test at command line enter:
  from rmh.test import dummyPatient
  dummyPatient.getDummyPatient()

Most patient keys are mined from raystation to a file with command:
  dummyPatient.writeKeys()

The file can then be added to with different patients loaded with this command:
  dummyPatient.appendKeys()

Using a range of different patients will make the record of patient keys more comprehensive
"""

# ------------------------------- #

from rmh.test import rslMocks
import os, clr

clr.AddReference("System.Drawing")
from System import Drawing

# ----- #

def addCase(pt):
    """
    Add an extra case to the patient
    """
    pt.Cases.append( pt.Cases[0].copy() )
    
# ----- #

def addExamination(case, Name='Image_1', PatientPosition='HFS', Modality='CT', FrameOfReference='1.2.345.67890', ImportFraction=0):
    """
    Add an Examination to the case
    """
    case.Examinations.append( case.Examinations[0].copy() )
    ind = len(case.Examinations) - 1
    
    case.Examinations[ind].Name = Name
    case.Examinations[ind].PatientPosition = PatientPosition
    case.Examinations[ind].Modality = Modality
    case.Examinations[ind].EquipmentInfo.FrameOfReference = FrameOfReference
    case.Examinations[ind].ImportFraction = ImportFraction
    
    addStructureSet(case, Examination=case.Examinations[ind])
    
# ----- #

def addPlan(case, Name='2PLAN', PlannedBy='ABC', FractionNumber=0 ):
    """
    Add a trestment plan to the case
    """
    case.TreatmentPlans.append( case.TreatmentPlans[0].copy() )
    ind = len(case.TreatmentPlans) - 1
    
    case.TreatmentPlans[ind].Name = Name
    case.TreatmentPlans[ind].PlannedBy = PlannedBy
    case.TreatmentPlans[ind].FractionNumber = FractionNumber
    
# ----- #

def addBeamSet(plan, DicomPlanLabel='1PLAN', PatientPosition='HeadFirstSupine', 
                Modality='Photons', DeliveryTechnique='Arc', FrameOfReference='1.2.345.67890',
                PlanGenerationTechnique='Imrt', PlanIntent='Undefined'):
    """
    Add another beamset to the plan
    """            
    plan.BeamSets.append( plan.BeamSets[0].copy() )
    ind = len(plan.BeamSets) - 1
    
    plan.BeamSets[ind].DicomPlanLabel = DicomPlanLabel
    plan.BeamSets[ind].Number = ind + 1
    plan.BeamSets[ind].PatientPosition = PatientPosition
    plan.BeamSets[ind].Modality = Modality
    plan.BeamSets[ind].DeliveryTechnique = DeliveryTechnique
    plan.BeamSets[ind].FrameOfReference = FrameOfReference
    plan.BeamSets[ind].PlanGenerationTechnique = PlanGenerationTechnique
    plan.BeamSets[ind].PlanIntent = PlanIntent
    
# ----- #

def addBeam(beamset, Name='1.1', Description='1.1 Arc', GantryAngle=179, 
                ArcRotationDirection='CounterClockwise', ArcStopGantryAngle=181,
                BeamMU=400.0, CouchAngle=0, InitialCollimatorAngle=5,
                CreatedDuringOptimization=True, HasValidSegments=True):
    """
    Add an extra beam into the beamset
    """
    beamset.Beams.append( beamset.Beams[0].copy() )
    ind = len(beamset.Beams) - 1
    
    beamset.Beams[ind].Name = Name
    beamset.Beams[ind].Description = Description
    beamset.Beams[ind].GantryAngle = GantryAngle
    beamset.Beams[ind].ArcRotationDirection = ArcRotationDirection
    beamset.Beams[ind].ArcStopGantryAngle = ArcStopGantryAngle
    beamset.Beams[ind].BeamMU = BeamMU
    beamset.Beams[ind].CouchAngle = CouchAngle
    beamset.Beams[ind].InitialCollimatorAngle = InitialCollimatorAngle
    beamset.Beams[ind].CreatedDuringOptimization = CreatedDuringOptimization
    beamset.Beams[ind].PatientPosition = beamset.PatientPosition
    beamset.Beams[ind].DeliveryTechnique = beamset.DeliveryTechnique
    beamset.Beams[ind].PlanGenerationTechnique = beamset.PlanGenerationTechnique
    beamset.Beams[ind].HasValidSegments = HasValidSegments
    
# ----- #

def addVmatSegment(beam, DeltaCouchAngle=0, DeltaGantryAngle=358):
    """
    Add a segment to a VMAT beam
    """
    beam.Segments.append( beam.Segments[0].copy() )
    ind = len(beam.Segments) - 1
    beam.Segments[ind].SegmentNumber = ind + 1
    beam.Segments[ind].DeltaCouchAngle = DeltaCouchAngle
    beam.Segments[ind].DeltaGantryAngle = DeltaGantryAngle
    
# ----- #

def addRigidRegistration(case, FromFrameOfReference='1.2.345.67890', 
                            ToFrameOfReference='1.2.345.67891', 
                            RigidTrandformationMatrix=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]):
    """
    Add a rigid registration
    """
    case.Registrations.append( case.Registrations[0].copy() )
    ind = len(case.Registrations) -1
    
    case.Registrations[ind].FromFrameOfReference = FromFrameOfReference
    case.Registrations[ind].ToFrameOfReference = ToFrameOfReference
    case.Registrations[ind].RigidTrandformationMatrix = RigidTrandformationMatrix

# ----- #

def addDeformableRegistration(case, Name='DefReg_1', RigidTransformation=None, 
                                FromExamName=None, ToExamName=None):  
    """
    Add a deformable registration
    """
    
    structRegGrps = case.PatientModel.StructureRegistrationGroups
    structRegGrps.append( structRegGrps[0].copy() )
    ind = len(structRegGrps) - 1
    
    if RigidTransformation is None:
        RigidTransformation = case.Registrations[0]
    if FromExamName is None:
        FromExamName = case.Examinations[0].Name
    if ToExamName is None:
        ToExamName = case.Examinations[1].Name
    
    structRegGrps[ind].Name = Name
    structRegGrps[ind].DeformableStructureRegistrations[0].Name = Name + '_1'
    structRegGrps[ind].DeformableStructureRegistrations[0].RigidTransformationMatrix = RigidTransformation.RigidTransformationMatrix
    structRegGrps[ind].DeformableStructureRegistrations[0].FromExamination.Name = FromExamName
    structRegGrps[ind].DeformableStructureRegistrations[0].ToExamination.Name = ToExamName
    
# ----- #

def addEvaluationDoses(case):
    """
    Make a set of Evaluation dose distributions
    """
    # Make evaluation dose distribution as calculated on first image
    frEval = case.TreatmentDelivery.FractionEvaluations[0]
    frEval.DoseOnExaminations[0].OnExamination.Name = pt.Cases[0].Examinations[0].Name
    frEval.DoseOnExaminations[0].DoseEvaluations[0].setID('000001')
    
    # Make extra evaluation dose distributions as calculated on each subsequent image
    dNum = 1
    for exam in case.Examinations[1:]:
        frEval.DoseOnExaminations.append(frEval.DoseOnExaminations[0].copy())
        frEval.DoseOnExaminations[ee].OnExamination.Name = exam.Name
        frEval.DoseOnExaminations[ee].DoseEvaluations[0].setID('%06d' % dNum)
        dNum += 1
        
    # On first image make deformed evaluation doses
    regGroups = case.PatientModel.StructureRegistrationGroups
    for exam, regGrp in zip(case.Examinations[1:], regGroups):
        doseEvals = frEval.DoseOnExaminations[0].DoseEvaluations
        doseEvals.append( doseEvals[0].copy() )
        ind = len(doseEvals) - 1
        
        doseEvals[ind].ByStructureRegistration = regGrp.DeformableStructureRegistrations[0]
        doseEvals[ind].setID('%06d' % dNum)
        dNum += 1
    
# ----- #

def addRegionOfInterest(case, Name='ROI_1', Color='Red', Type='Organ'):
    """
    Make a set of regions of interest
    """
    if type(Color) == str:
        Color = eval('Drawing.Color().%s' % Color)
    
    case.PatientModel.RegionsOfInterest.append( case.PatientModel.RegionsOfInterest[0].copy() )
    ind = len(case.PatientModel.RegionsOfInterest) - 1
    
    roi = case.PatientModel.RegionsOfInterest[ind]
    roi.Name = Name
    roi.Color = Color
    roi.Type = Type
    roi.RoiMaterial = None
    
    for exam in case.Examinations:
        if case.PatientModel.StructureSets[exam.Name].OnExamination != exam:
            addStructureSet(case, exam)
        sSet = case.PatientModel.StructureSets[exam.Name]
        addRoiGeometry(case, sSet, OfRoi=roi)
    
# ------------------------------- #

def addPointOfInterest(case, Name='POI_1', Color='Red', Type='Marker'):
    """
    Make a set of regions of interest
    """
    if type(Color) == str:
        Color = eval('Drawing.Color().%s' % Color)
    
    case.PatientModel.PointsOfInterest.append( case.PatientModel.PointsOfInterest[0].copy() )
    ind = len(case.PatientModel.PointsOfInterest) - 1
    
    poi = case.PatientModel.PointsOfInterest[ind]
    poi.Name = Name
    poi.Color = Color
    poi.Type = Type
    
    for exam in case.Examinations:
        if case.PatientModel.StructureSets[exam.Name].OnExamination != exam:
            addStructureSet(case, exam)
        sSet = case.PatientModel.StructureSets[exam.Name]
        addPoiGeometry(case, sSet, OfPoi=poi)

# ------------------------------- #

def addStructureSet(case, Examination=None):
    """
    Add a blank structure set for desired Examination 
    if one does not already exist.
    (if no Examination is provided choose the first Examination)
    """
    if Examination is None:
        Examination = case.Examinations[0]
    
    sSetExams = [ sSet.OnExamination.Name for sSet in case.PatientModel.StructureSets ]
    
    if Examination in sSetExams:
        return
    
    case.PatientModel.StructureSets.append( case.PatientModel.StructureSets[0].copy() )
    ind = len(case.PatientModel.StructureSets) - 1
    
    case.PatientModel.StructureSets[ind].OnExamination = Examination
    case.PatientModel.StructureSets[ind].ApprovedStructureSets = rslMocks.RslSequence()
    
    for rr, r0 in enumerate(case.PatientModel.StructureSets[0].RoiGeometries):
        case.PatientModel.StructureSets[ind].RoiGeometries[rr].OfRoi = r0.OfRoi
    
# ------------------------------- #
    
def addRoiGeometry(case, sSet, OfRoi=None):
    """
    Add a blank ROI geometry to a structure set if one does not already exist.
    (if no Roi is provided choose the first Roi)
    """
    if OfRoi is None:
        OfRoi = case.PatientModel.RegionsOfInterest[0]
    sSetRois = [ rGeom.OfRoi.Name for rGeom in sSet.RoiGeometries ]
    
    if OfRoi.Name in sSetRois:
        return
        
    sSet.RoiGeometries.append( sSet.RoiGeometries[0].copy() )
    ind = len(sSet.RoiGeometries) - 1
    
    sSet.RoiGeometries[ind].OfRoi = OfRoi
    
# ------------------------------- #

def addPoiGeometry(case, sSet, OfPoi=None):
    """
    Add a blank POI geometry to a structure set if one does not already exist.
    (if no Poi is provided choose the first Poi)
    """
    if OfPoi is None:
        OfPoi = case.PatientModel.PointsOfInterest[0]
    
    sSetPois = [ pGeom.OfPoi.Name for pGeom in sSet.PoiGeometries ]
    
    if OfPoi.Name in sSetPois:
        return
        
    sSet.PoiGeometries.append( sSet.PoiGeometries[0].copy() )
    ind = len(sSet.PoiGeometries) - 1
    
    sSet.PoiGeometries[ind].OfPoi = OfPoi
    
# ------------------------------- #

def addMaterial(case, BaseOnMaterial=None, Name='Material_1', MassDensityOverride='1.0'):
    """
    Add a material to the list of materials in the case
    """
    if BaseOnMaterial is None:
        BaseOnMaterial = case.PatientModel.Materials[0]
    
    case.PatientModel.Materials.append( BaseOnMaterial.copy() )
    ind = len(case.PatientModel.Materials) - 1
    
    case.PatientModel.Materials[ind].Name = Name
    case.PatientModel.Materials[ind].MassDensity = MassDensityOverride
    
# ------------------------------- #

def approveROIs(case, ROINames=[], exam=None):
    """
    Add approval stamp to given ROI Names
    """
    if exam is None:
        exam = case.Examinations[0]
        
    sSet = case.PatientModel.StructureSets[exam.Name]
    if sSet.ApprovedStructureSets is None:
        sSet.ApprovedStructureSets = rslMocks.RslSequence()
    
    if len(sSet.ApprovedStructureSets) < 1:
        sSet.ApprovedStructureSets.append( 
            rslMocks.AttrDict(
                {'ApprovedRoiStructures':rslMocks.RslSequence()}
            ) 
        )
        
    if sSet.ApprovedStructureSets[0].ApprovedRoiStructures is None:
        sSet.ApprovedStructureSets[0].ApprovedRoiStructures = rslMocks.RslSequence()
    
    for roiName in ROINames:
        sSet.ApprovedStructureSets[0].ApprovedRoiStructures.append( 
            rslMocks.AttrDict(
                {'OfRoi' : rslMocks.AttrDict({'Name':roiName})}
            )
        )
    
# ------------------------------- #

def approvePOIs(case, POINames=[], exam=None):
    """
    Add approval stamp to given POI Names
    """
    if exam is None:
        exam = case.Examinations[0]
        
    sSet = case.PatientModel.StructureSets[exam.Name]
    if sSet.ApprovedStructureSets is None:
        sSet.ApprovedStructureSets = rslMocks.RslSequence()
    
    if len(sSet.ApprovedStructureSets) < 1:
        sSet.ApprovedStructureSets.append( 
            rslMocks.AttrDict(
                {'ApprovedRoiStructures':rslMocks.RslSequence()}
            ) 
        )
        
    if sSet.ApprovedStructureSets[0].ApprovedRoiStructures is None:
        sSet.ApprovedStructureSets[0].ApprovedRoiStructures = rslMocks.RslSequence()
    
    for poiName in POINames:
        sSet.ApprovedStructureSets[0].ApprovedPoiStructures.append( 
            rslMocks.AttrDict(
                {'OfPoi' : rslMocks.AttrDict({'Name':poiName})}
            )
        )

# ------------------------------- #

def approvePlan(plan):
    """
    Add approval stamp to given plan
    """
    plan.Review = rslMocks.AttrDict({'ApprovalStatus':'Approved'})
    
# ------------------------------- #
