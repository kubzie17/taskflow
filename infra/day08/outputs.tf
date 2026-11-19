output "security_group_id" {
  description = "Private ledger: inspect this group in EC2."
  value       = aws_security_group.pilot.id
}

output "instance_id" {
  description = "Private ledger: host for the next session when enabled."
  value       = try(aws_instance.pilot[0].id, null)
}

output "availability_zone" {
  value = data.aws_subnet.assigned.availability_zone
}

output "node_role_name" {
  description = "Course-managed role; for a supplied profile ask the owner for the underlying role name."
  value       = try(aws_iam_role.pilot[0].name, null)
}

output "data_volume_id" {
  description = "Private ledger: separately managed bookings data volume."
  value       = try(aws_ebs_volume.bookings[0].id, null)
}

output "release_stage" {
  description = "ReleaseStage tag on the managed security group."
  value       = aws_security_group.pilot.tags["ReleaseStage"]
}
