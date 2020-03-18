package Constraints

import oscar.cp.core.variables.{CPIntVar, CPVar}
import oscar.cp.core.{CPPropagStrength, Constraint}

import scala.collection.Iterable

class CstDummy(val decisionParent: CPIntVar, val decisionChildLeft: CPIntVar, val decisionChildRight: CPIntVar, val sumChildLeft: CPIntVar, val sumChildRight: CPIntVar) extends Constraint(decisionParent.store, "NodeLink2") {

  override def associatedVars(): Iterable[CPVar] = Array(decisionParent, decisionChildLeft, decisionChildRight, sumChildLeft, sumChildRight)

  /**
    *
    * @param l
    * @return CPOutcome state
    */
  override def setup(l: CPPropagStrength): Unit = {
    decisionParent.callPropagateWhenBoundsChange(this)
    propagate()
  }

  /**
    *
    * @return CPOutcome state
    */
  override def propagate(): Unit = {
    if (decisionParent.max == 0) {
      decisionChildLeft.assign(0)
      decisionChildRight.assign(0)
      this.deactivate()
    } else if (decisionParent.min > 0) {
      sumChildRight.removeValue(0)
      sumChildLeft.removeValue(0)
      this.deactivate()
    }
  }


}

class CstDummyEnd(val decisionParent: CPIntVar, val sumChildLeft: CPIntVar, val sumChildRight: CPIntVar) extends Constraint(decisionParent.store, "NodeLink2") {

  override def associatedVars(): Iterable[CPVar] = Array(decisionParent, sumChildLeft, sumChildRight)

  /**
    *
    * @param l
    * @return CPOutcome state
    */
  override def setup(l: CPPropagStrength): Unit = {
    decisionParent.callPropagateWhenBoundsChange(this)
    propagate()
  }

  /**
    *
    * @return CPOutcome state
    */
  override def propagate(): Unit = {
    if (decisionParent.min > 0) {
      sumChildRight.removeValue(0)
      sumChildLeft.removeValue(0)
      this.deactivate()
    }
  }


}
