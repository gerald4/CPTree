package DecisionTree

import DataManipulation.Data
import oscar.cp.core.variables.CPIntVar
import oscar.cp.{CPStore, minimum}

class DLeaf(
             solver: CPStore,
             db: Data,
             id: Int
           ) extends DTree(0, solver, db, id) {


  val auxiliaryVariables: Array[CPIntVar] = Array(countM, countP, countSum, miniSum)

  /**
    * Apply Functions
    */
  def applyToAllTree(fct: DTree => Unit): Unit = fct(this)

  def applyToAllNode(fct: DTreeDecision => Unit): Unit = {}

  def applyToNode(fct: DNode => Unit): Unit = {}

  def applyToEndNode(fct: DEndNode => Unit): Unit = {}

  def applyToLeaf(fct: DLeaf => Unit): Unit = fct(this)

  /**
    * Constraints
    */
  // miniSum = miniSum_left + miniSum_right if decision node
  // miniSum = min(countP,countM) if leaf
  def _addCstMiniSum: Unit =
    solver.add(minimum(Array(countP, countM), miniSum))

  /**
    * Applying constraints
    */
  // right-most leaf countSum > 0 in any case
  def cstLeftMostCountSum: Unit =
    this._addNodeNonEmpty

  /**
    * Print
    */

  def toStringTree(): String =
    toStringTreeLeaf()



  /**
    * TODO Rm?
    */
  def fillBFSAllTree[T](fct: DTree => T, array: Array[T], spot: Int): Unit =
    array(spot) = fct(this)

  def fillBFSAllNode[T](fct: DTreeDecision => T, array: Array[T], spot: Int): Unit = {}

}

