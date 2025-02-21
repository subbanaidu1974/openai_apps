import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ApplicantComponent } from './applicant/applicant.component';
import { EmploymentComponent } from './employment/employment.component';
import { SpouseCoApplicantComponent } from './spousecoapplicant/spousecoapplicant.component';
import { RaceEthnicityComponent } from './raceethnicity/raceethnicity.component';
import { OtherHouseholdMembersComponent } from './otherhouseholdmembers/otherhouseholdmembers.component';
import { HouseholdIncomeComponent } from './householdincome/householdincome.component';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'applicant', component: ApplicantComponent}
];

// const routes: Routes = [
//   { path: '', component: HomeComponent },
//   { path: 'applicant', component: ApplicantComponent },
//   { path: 'spousecoapplicant', component: SpouseCoApplicantComponent },
//   { path: 'raceethnicity', component: RaceEthnicityComponent },
//   { path: 'otherhouseholdmembers', component: OtherHouseholdMembersComponent },
//   { path: 'householdincome', component: HouseholdIncomeComponent},
//   { path: 'employment', component: EmploymentComponent },
//   { path: '**', redirectTo: '', pathMatch: 'full' } // Redirect to home for any unknown routes
// ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

